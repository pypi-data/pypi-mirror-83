#!/usr/bin/python3
# -*- coding: utf-8 -*-

import copy
import time
import json
import tempfile
import traceback
import threading

from gfaaccesslib import logger
from gfaaccesslib.gfa import GFA, API_VERSION
from gfaaccesslib.api_helpers import  GFAStackCodops
from gfafunctionality.raws import RawImageFile, RawImageMetadata

from enum import Enum


class Storage(Enum):
    read = 0
    dump = 1
    move = 2


class Test(Enum):
    NONE = 0
    BIAS = 1
    DC = 2
    FCTE = 3
    PTC = 4
    FLATS = 5
    DARKS = 6
    LIFE = 7
    PSF = 8
    PSF_LOOPING = 9


class Config:

    def __init__(self, metadata, is_save=False, out_dir='/tmp', pattern=0, mode=0, is_fake=False,
                 storage=Storage.read, is_clear=False, test=Test.NONE, image_name="", ptc_type=0, show_plot=True):

        self.is_save = is_save
        self.is_clear = is_clear
        self.is_fake = is_fake
        self.out_dir = out_dir
        self.pattern = pattern
        self.mode = mode
        self.metadata = metadata
        self.storage = storage
        self.test = test
        self.image_name = image_name
        self.ptc_type = ptc_type
        self.show_plot = show_plot


class Shutter:

    def __init__(self, cfg, stack):
        self._shutter_on = cfg.metadata.exptime != 0 and cfg.test != Test.DC and cfg.test != Test.DARKS and cfg.ptc_type != 2
        self._stack = stack

    def __enter__(self):
        if self._shutter_on:
            self._stack.add_open_shutter_command()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._shutter_on:
            self._stack.add_close_shutter_command()


class TimeDiff:

    def __init__(self):
        self._start = None
        self._end = None

    def start(self):
        self._start = time.time()

    def end(self):
        self._end = time.time()

    def diff(self):
        # Not launched by us, so we don't measure it
        if not self._start or not self._end:
            return None

        return round(self._end - self._start, 3)


class GFAWrapper:

    # All parameters are callback to the GUI functions
    def __init__(self):
        self._gui_img_start_cb = lambda: None
        self._gui_img_done_cb = lambda: None
        self._gui_sensors_cb = lambda: None
        self._gui_err_cb = lambda: None

        self._gfa = None
        self._logfile = tempfile.NamedTemporaryFile()
        self._is_error = False
        self._elapsed_exp_time = TimeDiff()
        self._tests_cv = threading.Condition()
        self._psf_looping_counter = 0

        self.log_file_name = self._logfile.name
        self.cfg = None

        # Add a file handler so the GUI can read all the logs
        logger.add_file_handler(self.log_file_name)

        self._gfa = GFA("", 1, 1, auto_connect_async=False, auto_update=False)

    def _start_adc(self):
        self.write_spi_adc(0xf, 0x0)
        self._gfa.adccontroller.adc_start_acq()

    def _read_rows(self, rows_number):
        self._gfa.clockmanager.stack.add_read_rows_cmd(rows_number)

    def _dump_rows(self, rows_number):
        self._gfa.clockmanager.stack.add_dump_rows_cmd(rows_number)

    def _move_rows(self, rows_number):
        self._gfa.clockmanager.stack.add_accumulate_rows_cmd(rows_number)

    def _set_scan_values(self, overscan, prescan, columns):
        self._gfa.clockmanager.geom_conf.overscan_cols = overscan
        self._gfa.clockmanager.geom_conf.prescan_cols = prescan
        self._gfa.clockmanager.geom_conf.amplifier_active_cols = columns
        self._gfa.clockmanager.remote_set_ccd_geom()

    def _define_expose(self):
        # It is critic to close the async thread when out of the script
        # Before taking an exposure we have to define it
        # we can do it manually, taking the stack and filling it:
        # If we don't set an image_id, it will update its internal counter
        g = self._gfa.clockmanager.stack
        g.add_new_image_cmd()
        #g.add_set_modes_cmd(True, True, True, True)

    def _exp_start_cb(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)

        # if "mode" in j:
        #    self.cfg.mode = j["mode"]
        self._gui_img_start_cb(header, j)

    def _exp_end_cb(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)

        if self.cfg.test != Test.PSF_LOOPING:
            if not self.cfg:
                metadata = RawImageMetadata(0, 0, 0, 0, 0, 0, "NONE")
                self.cfg = Config(metadata)

            if "provider" in j:
                self.cfg.is_fake = True if j["provider"] == 1 else False

            if "mode" in j:
                self.cfg.mode = 0 if self.cfg.is_fake else j["mode"]
                self.cfg.pattern = j["mode"]

            if "amplifier_active_cols" in j:
                self.cfg.metadata.columns = j["amplifier_active_cols"]

            if "overscan_cols" in j:
                self.cfg.metadata.overscan = j["overscan_cols"]

            if "prescan_cols" in j:
                self.cfg.metadata.prescan = j["prescan_cols"]

            total_rows = 0
            if "commands_uint" in j:
                for cmd in j["commands_uint"]:
                    if (cmd >> 27) == int(GFAStackCodops.wait, 2):
                        ms = cmd & 0x00ffffff
                        self.cfg.metadata.exptime = ms/1000
                    elif (cmd >> 27) == int(GFAStackCodops.proc_rows, 2):
                        total_rows += cmd & 0x0000ffff
                        if (cmd >> 24) == 0b00011100:
                            self.cfg.storage = Storage.dump
                        elif (cmd >> 24) == 0b00011010:
                            self.cfg.storage = Storage.move
                        elif (cmd >> 24) == 0b00011000:
                            self.cfg.storage = Storage.read
                        elif (cmd >> 24) == 0b00011001:
                            # ¿?
                            self.cfg.storage = Storage.read

            self.cfg.metadata.num_rows = total_rows

        if self._is_error:
            self._is_error = False
            return

        try:
            self._elapsed_exp_time.end()
            im_num = sorted(self._gfa.raws.list_images())[-1]
            im = self._gfa.raws.get_image(im_num)

            if self.cfg and self.cfg.is_save:
                if self.cfg.test == Test.PSF_LOOPING:
                    self.cfg.image_name = "PSF_{:0>3}".format(self._psf_looping_counter)
                    self._psf_looping_counter += 1

                if self.cfg.image_name != "":
                    im_name = self.cfg.image_name
                else:
                    im_name = 'IMG_{}'.format(im_num)

                raw = RawImageFile(im, self.cfg.metadata)

                if self.cfg.mode == 4:
                    # Save data as a CSV
                    raw.save_waveform_table(self.cfg.out_dir, im_name)
                else:
                    raw.save_fits(self.cfg.out_dir, im_name)


            # If we were taking several images, probably it would be a good
            # idea to remove images we don't need anymore
            self._gfa.raws.rem_image(im_num)

            self._gui_img_done_cb(im, self.cfg, self._elapsed_exp_time.diff())

            if self.cfg and self.cfg.test != Test.NONE and self.cfg.test != Test.PSF_LOOPING:
                with self._tests_cv:
                    self._tests_cv.notify()

        except Exception as ex:
            traceback.print_exc()
            self._gui_err_cb(str(ex))

    def _error_cb(self, header, data):
        self._is_error = True
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)
        msg = j["msg"]
        self._gui_err_cb(msg)

    def _telem_cb(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)
        self._gui_telem_cb(j)

    def _sensors_cb(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)
        self._gui_sensors_cb(j)

    def _pid_cb(self, header, data):
        if isinstance(data, bytes):
            data = data.decode('UTF-8')
        j = json.loads(data)
        self._gui_pid_cb(j)

    def configure_callbacks(self, img_start, img_done, sensors, error, pid):
        self._gui_img_start_cb = img_start
        self._gui_img_done_cb = img_done
        self._gui_sensors_cb = sensors
        self._gui_err_cb = error
        self._gui_pid_cb = pid

        self._gfa.async_manager.add_new_image_callback(self._exp_start_cb)
        self._gfa.async_manager.add_sensors_reading_callback(self._sensors_cb)
        self._gfa.async_manager.add_end_image_callback(self._exp_end_cb)
        self._gfa.async_manager.add_error_callback(self._error_cb)
        self._gfa.async_manager.add_pid_callback(self._pid_cb)

    def is_same_api(self):
        return self._gfa.sys.remote_api().answer["version"] == API_VERSION

    def set_config(self, conf):
        self.cfg = copy.deepcopy(conf)

    def connect(self, ip, port, aport):
        if ip != "":
            self._gfa.connect(ip, port, aport)

        self._gfa.remote_update()

    def power_up(self):
        self._gfa.exposecontroller.remote_power_up()

    def power_down(self):
        self._gfa.exposecontroller.remote_power_down()

    def clear_error(self):
        self._gfa.exposecontroller.remote_clear_error_state()

    def configure(self):
        self._gfa.clockmanager.remote_set_ccd_geom()
        self._gfa.clockmanager.remote_set_clock_timings()

        self._gfa.powercontroller.remote_set_dac_conf()

        self._gfa.powercontroller.voltages.set_default_values()
        self._gfa.powercontroller.remote_set_voltages()

        self._gfa.powercontroller.powerup_timing_ms = 250
        self._gfa.powercontroller.remote_set_phase_timing()

        exp = self._gfa.exposecontroller
        exp.remote_power_up()

        itr = 0
        while exp.status.ready_state is False:
            if itr > 30:
                fmt = "gfa is not in ready state. current_state: {}".format(exp.status.current_state)
                raise Exception(fmt)
            time.sleep(0.5)
            exp.remote_get_status()
            itr += 1

        self._gfa.powercontroller.remote_set_phase_timing()

        # Set Gain of ADC to 0db
        self.write_spi_adc(0x2a, 0x0)
        # Previously, gain was set to 12dB
        # gfa.adccontroller.spi_write(0x2a, 0xcccc)

    def close(self):
        self.disconnect()

    def unconfigure(self):
        exp = self._gfa.exposecontroller

        self._gfa.powercontroller.powerdown_timing_ms = 1000
        self._gfa.powercontroller.remote_set_phase_timing()
        exp.remote_power_down()
        self._gfa.adccontroller.set_adc_powerdown_pin(True)

        itr = 0
        while exp.status.configured_state is False \
                and exp.status.error_state is False \
                and exp.status.idle_state is False:
            if itr > 30:
                fmt = "gfa is not in configured state. current_state: {}".format(exp.status.current_state)
                raise Exception(fmt)
            time.sleep(0.5)
            exp.remote_get_status()
            itr += 1

    def disconnect(self):
        if self._gfa:
            self._gfa.close()

    def clear_stack(self):
        self._gfa.clockmanager.stack.clear()

    def clear_buff(self):
        self._gfa.buffers.remote_clear_buffers()

    def calibrate_adc(self):
        self._gfa.adccontroller.set_adc_reset_pin(0)
        self._gfa.adccontroller.set_adc_reset_pin(1)
        self._gfa.adccontroller.set_adc_powerdown_pin(False)
        self._gfa.adccontroller.reset_adc_controller()

        self._gfa.adccontroller.adc_init_calib()
        self._gfa.adccontroller.remote_get_status()
        if self._gfa.adccontroller.status.init_status.state != 's_init':
            raise Exception('System should be at calibration')

        # reset adc chip by spi
        self.write_spi_adc(0x0, 0x1)
        time.sleep(0.1)
        self.write_spi_adc(0x0, 0x0)
        time.sleep(0.1)

        # configure serialization on adc
        self.write_spi_adc(0x46, 0x8801)

        # set expected data pattern
        self._gfa.adccontroller.remote_set_init_rx_expected_pattern(0xf0f0)

        # set adc to output sync pattern
        time.sleep(0.1)
        self.write_spi_adc(0x45, 0x2)

        # start align frame
        self._gfa.adccontroller.adc_calib_align_frame()

        # check it has finished aligning frame
        for i in range(10):
            self._gfa.adccontroller.remote_get_status()
            if self._gfa.adccontroller.status.init_status.frame_aligned:
                break
        else:
            raise Exception('Frame could not be aligned')

        self._gfa.adccontroller.adc_calib_align_data()

        self._gfa.adccontroller.adc_calib_bitslip()

        self._gfa.adccontroller.remote_get_status()
        self._gfa.adccontroller.remote_get_init_rx_expected_pattern()
        self._gfa.adccontroller.remote_get_init_rx_data()

        # remove pattern
        self.write_spi_adc(0x45, 0x0)

        self._gfa.adccontroller.adc_stop_calib()

    def set_adc_delay(self, clock_steps):
        self._gfa.buffers.adc_delay = clock_steps

    def get_adc_delay(self):
        return self._gfa.buffers.adc_delay

    def enable_drivers(self):
        self._gfa.adccontroller.remote_enable_drivers()

    def disable_drivers(self):
        self._gfa.adccontroller.remote_disable_drivers()

    def enable_discharge(self, duration, pixel_start, reset_start):
        self._gfa.clockmanager.remote_enable_discharge(duration, pixel_start, reset_start)

    def disable_discharge(self):
        self._gfa.clockmanager.remote_disable_discharge()

    def write_spi_adc(self, address, value):
        self._gfa.adccontroller.spi_write(address, value)

    def write_gain_adc(self, ch1, ch2, ch3, ch4):
        val = ch1 | (ch2 << 4) | (ch3 << 8) | (ch4 << 12)
        self.write_spi_adc(0x2a, val)

    def write_spi_offsets(self, address, value, spd, pwr):
        # 2 LSB don't care
        data = 0b0000000000000000
        data |= address << 14
        data |= int(pwr) << 13
        data |= int(spd) << 12
        data |= value << 2
        self._gfa.powercontroller.remote_spi_write(data)

    def get_geom_conf(self):
        self._gfa.clockmanager.remote_get_ccd_geom()
        return self._gfa.clockmanager.geom_conf

    def set_geom_conf(self):
        self._gfa.clockmanager.remote_set_ccd_geom()

    def get_clk_timings(self):
        self._gfa.clockmanager.remote_get_clock_timings()
        return self._gfa.clockmanager.time_conf

    def set_clk_timings(self):
        self._gfa.clockmanager.remote_set_clock_timings()

    def get_reg_info(self):
        self._gfa.clockmanager.remote_get_info()
        return self._gfa.clockmanager.info

    def get_dac_voltages(self):
        self._gfa.powercontroller.remote_get_configured_voltages()
        return self._gfa.powercontroller.voltages

    def get_expctrl_info(self):
        self._gfa.exposecontroller.remote_get_status()
        return self._gfa.exposecontroller.status

    def get_vlt_enables(self):
        self._gfa.powercontroller.remote_get_enables()
        return self._gfa.powercontroller.enables

    def get_phase_timings(self):
        self._gfa.powercontroller.remote_get_phase_timing()
        return self._gfa.powercontroller.powerup_timing_ms

    def get_configured_channels(self):
        self._gfa.powercontroller.remote_get_configured_channels()
        return self._gfa.powercontroller.dac_channels

    def get_irq_status(self):
        self._gfa.irq.remote_get_status()
        return self._gfa.irq.status

    def get_buffers_status(self):
        self._gfa.buffers.remote_get_buffers_status()
        return self._gfa.buffers.status

    def request_telemetry(self):
        self._gfa.exposecontroller.remote_get_telemetry()

    def expose(self):
        self._start_adc()

        meta = self.cfg.metadata
        self._set_scan_values(meta.overscan, meta.prescan, meta.columns)

        self.clear_stack()
        self._define_expose()

        g = self._gfa.clockmanager.stack

        if self.cfg.is_clear:
            self._dump_rows(1024)
        with Shutter(self.cfg, g):
            g.add_wait_cmd(int(meta.exptime * 1000))

        if self.cfg.storage == Storage.read:
            self._read_rows(meta.storage_rows)
        if self.cfg.storage == Storage.dump:
            self._dump_rows(meta.storage_rows)
        if self.cfg.storage == Storage.move:
            self._move_rows(meta.storage_rows)

        self._read_rows(meta.active_rows)

        self._gfa.clockmanager.stack.add_none_cmd()
        # Then we have to set to GFA
        self._gfa.clockmanager.remote_set_stack_contents()

        # If we are playing with the simulator and want to receive something that is not
        # zeros, we have to set which pattern do we want:
        if self.cfg.is_fake:
            self._gfa.buffers.remote_set_data_provider(1, self.cfg.pattern)
        else:
            self._gfa.buffers.remote_set_data_provider(0, self.cfg.mode)

        self._elapsed_exp_time.start()

        self._gfa.exposecontroller.remote_start_stack_exec()

        if self.cfg.test != Test.NONE:
            with self._tests_cv:
                self._tests_cv.wait()

    def expose_loop(self, num):
        self._start_adc()

        meta = self.cfg.metadata
        EXPOSE_TIME_IN_10NS = meta.exptime * 1000 * 100000
        print("EXPTIME=", EXPOSE_TIME_IN_10NS)
        self._set_scan_values(meta.overscan, meta.prescan, meta.columns)

        self.clear_stack()

        g = self._gfa.clockmanager.stack

        # Clear and start TR15, the one that holds the whole duration of this stack running
        g.add_tr_clear(15, all=False)
        g.add_tr_start_timer(15, '1ms')
        # Load desired number of images to TR3
        g.add_tr_load_value(tr_address=3, value=num)
        # Clear image counter( TR4)
        g.add_tr_clear(tr_address=4, all=False)

        # Enable all amplifiers and both image and storage vertical clocks
        g.add_set_modes_cmd(True, True, True, True)
        # Clear TR0
        g.add_tr_clear(0, all=False)
        # Clear TR2
        g.add_tr_clear(2, all=False)
        # Load desired expose time in TR1
        g.add_tr_load_value(1, EXPOSE_TIME_IN_10NS)  # 2 seconds in 10ns units
        # Clear CCD : Dump all rows
        g.add_dump_rows_cmd(self._gfa.clockmanager.geom_conf.total_rows)
        # start timer 0 - the one which is used to control image exposure time
        g.add_tr_start_timer(0, resolution='10ns')

        #####################################################
        g.add_loop_start()

        # wait expose time:
        g.add_wait_until_tra_goet_trb_cmd(address_tra=0, address_trb=1)
        # save time exposed to TR20
        g.add_tr_copy_trb_2_tra(trb_address=0, tra_address=20)
        # Save timestamp of end expose
        # add_copy_ts(stack=g, tr_ts_sec=17, tr_ts_ms=16, tr_dest_sec=14, tr_dest_ms=13)
        # We start the new_exposure here, otherwise, it doesn't counts the dump of rows to
        # the rows processed counter
        g.add_new_image_cmd()
        # start timer 2 to know transfer time
        # Here TR2 has been cleared
        g.add_tr_start_timer(2, resolution='10ns')
        # Transfer image to storage: Dump storage rows
        g.add_dump_rows_cmd(self._gfa.clockmanager.geom_conf.storage_rows)
        # Copy tr2 to tr 19
        g.add_tr_copy_trb_2_tra(tra_address=19, trb_address=2)
        # Clear TR2
        g.add_tr_clear(2, all=False)
        # Clear TR0
        g.add_tr_clear(0, all=False)

        # Exposing time for next image starts here. Start timer 0
        g.add_tr_start_timer(0, resolution='10ns')

        # Disable image vertical clocks
        g.add_set_modes_cmd(eh_en=True, fg_en=True, image_en=False, storage_en=True)

        # start timer 2 to know readout time
        g.add_tr_start_timer(2, resolution='10ns')

        # Read out image section
        g.add_read_rows_cmd(self._gfa.clockmanager.geom_conf.image_rows)

        # Copy readout time to tr 18
        g.add_tr_copy_trb_2_tra(tra_address=18, trb_address=2)
        # Clear TR2
        g.add_tr_clear(2, all=False)
        # Save timestamp of end readout
        # add_copy_ts(stack=g, tr_ts_sec=17, tr_ts_ms=16, tr_dest_sec=12, tr_dest_ms=11)

        # Mark end of the read image
        g.add_end_image_cmd()

        # Enable all amplifiers and both image and storage vertical clocks
        g.add_set_modes_cmd(True, True, True, True)

        # Increase image counter
        g.add_tr_increase(tr_address=4)
        # loop if TR4 >= TR3, externally set TR3 to 0 to stop looping
        g.add_loop_end_loop_if_tra_loet_trb(tra_address=3, trb_address=4)

        # Out of the loop, stop timer of full duration ot stack running
        g.add_tr_stop_timer(15)

        g.add_none_cmd()
        # Then we have to set to GFA
        self._gfa.clockmanager.remote_set_stack_contents()

        # If we are playing with the simulator and want to receive something that is not
        # zeros, we have to set which pattern do we want:
        if self.cfg.is_fake:
            self._gfa.buffers.remote_set_data_provider(1, self.cfg.pattern)
        else:
            self._gfa.buffers.remote_set_data_provider(0, self.cfg.mode)

        if self.cfg.test != Test.PSF_LOOPING:
            self._elapsed_exp_time.start()

        self._gfa.exposecontroller.remote_start_stack_exec()

        if self.cfg.test != Test.NONE:
            if self.cfg.test == Test.PSF_LOOPING:
                print("SLEEP=", num * EXPOSE_TIME_IN_10NS / 100000000.0 + 15)
                time.sleep(num * EXPOSE_TIME_IN_10NS / 100000000.0 + 15)  # 60 hours
                print(self._psf_looping_counter)
                self._gfa.clockmanager.remote_set_tr_value(value=0, tr_addr=3)
            else:
                with self._tests_cv:
                    self._tests_cv.wait()

