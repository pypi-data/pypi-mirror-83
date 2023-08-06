import os
import time
import threading
from datetime import datetime

import gfagui.gfa


class Tests:

    def __init__(self, gfa_instance, exp_conf):

        self._gfa = gfa_instance
        self._exp_cfg = exp_conf
        self._base_out_dir = self._exp_cfg.out_dir
        self._test_thread = threading.Thread()

        self.stop_life_test = False

        if exp_conf.test == gfa.Test.NONE:
            raise Exception("Not a test")

    def _run_expose_loop(self, number, name):
        for i in range(number):
            self._exp_cfg.image_name = "{}_{:0>3}".format(name, i)
            self._gfa.expose(self._exp_cfg)

    def _run_ptc_test(self):
        image_counter = 0
        exp_time = 0
        while exp_time <= 15:
            self._exp_cfg.metadata.exptime = exp_time

            self._exp_cfg.ptc_type = 1
            for i in range(2):
                self._exp_cfg.image_name = "PTC_{:0>3}".format(image_counter)
                image_counter += 1
                self._gfa.expose(self._exp_cfg)

            self._exp_cfg.ptc_type = 2
            for i in range(2):
                self._exp_cfg.image_name = "PTC_{:0>3}".format(image_counter)
                image_counter += 1
                self._gfa.expose(self._exp_cfg)
            exp_time += 2

        self._exp_cfg.ptc_type = 0

    def _run_fcte_test(self):
        self._exp_cfg.metadata.exptime = 7
        self._run_expose_loop(10, "FCTE")

    def _run_bias_test(self):
        self._exp_cfg.metadata.exptime = 0
        self._run_expose_loop(10, "BIAS")

    def _run_dc_test(self):
        self._exp_cfg.metadata.exptime = 60
        self._run_expose_loop(10, "DARKS")

    def _run_life_test(self):
        self._exp_cfg.is_save = 0
        start = datetime.now()
        n = 0
        while not self.stop_life_test:
            self._exp_cfg.image_name = "{}_{:0>3}".format(self._exp_cfg.test.name, n)
            self._gfa.expose(self._exp_cfg)

            self._exp_cfg.is_save = 0

            now = datetime.now()

            diff = int((now - start).total_seconds())
            if diff >= 60*60: # each hour save an image
                self._exp_cfg.is_save = 1
                start = datetime.now()

            n += 1

            time.sleep(60)

    def _run_psf_test(self):
        img_number = 0
        for i in [0, 2, 3, 4, 6, 8, 10]:
            for j in range(2):
                self._exp_cfg.metadata.exptime = i
                self._exp_cfg.image_name = "PSF_{:0>3}".format(img_number)
                self._gfa.expose(self._exp_cfg)
                img_number += 1

    def _run_psf_looping_test(self):
        img_number = 0
        for i in [3, 4, 6, 8, 10]:
            self._exp_cfg.metadata.exptime = i
            self._exp_cfg.image_name = "PSF_{:0>3}".format(img_number)
            self._gfa._do_expose(self._exp_cfg, 5)
            img_number += 5


    def _run(self):
        self._exp_cfg.is_save = 1
        self._exp_cfg.is_clear = True

        if self._exp_cfg.test == gfa.Test.PTC:
            self._create_output_directory()
            self._run_ptc_test()
        elif self._exp_cfg.test == gfa.Test.DC:
            self._create_output_directory()
            self._run_dc_test()
        elif self._exp_cfg.test == gfa.Test.FCTE:
            self._create_output_directory()
            self._run_fcte_test()
        elif self._exp_cfg.test == gfa.Test.BIAS:
            self._create_output_directory()
            self._run_bias_test()
        elif self._exp_cfg.test == gfa.Test.FLATS:
            self._create_output_directory()
            self._run_ptc_test()
            self._create_output_directory()
            self._run_fcte_test()
        elif self._exp_cfg.test == gfa.Test.DARKS:
            self._create_output_directory()
            self._run_bias_test()
            self._create_output_directory()
            self._run_dc_test()
        elif self._exp_cfg.test == gfa.Test.LIFE:
            self._create_output_directory()
            self._run_life_test()
        elif self._exp_cfg.test == gfa.Test.PSF:
            self._create_output_directory()
            self._run_psf_test()
        elif self._exp_cfg.test == gfa.Test.PSF_LOOPING:
            self._create_output_directory()
            self._run_psf_looping_test()
        else:
            raise Exception("No tests were executed")

    def _create_output_directory(self):
        # Make a new folder for each launched test
        now = datetime.now()
        subfolder_name = now.strftime('%Y%m%d_%H%M%S')
        self._exp_cfg.out_dir = os.path.join(self._base_out_dir, subfolder_name)
        os.makedirs(self._exp_cfg.out_dir, exist_ok=True)

    def run(self):
        if self._test_thread.is_alive():
            self._test_thread.join()

        self._test_thread = threading.Thread(target=self._run)

        self._test_thread.start()
