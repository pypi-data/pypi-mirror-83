#!/usr/bin/python3
# -*- coding: utf-8 -*-

from guiqwt.builder import make
from guiqwt.styles import CurveParam
from guiqwt.curve import CurveItem

from gfafunctionality.raws import RawRepresentation
from pyqt_tools import table_operations


def save_current_config_table(tab_widget, conf):
    table = tab_widget.config_table
    item_number = 0

    def add_item(string, val):
        nonlocal item_number
        table_operations.create_item(table, item_number, string, val)
        item_number += 1

    add_item("Fake Data", conf.is_fake)
    add_item("Expose Time", conf.metadata.exptime)
    add_item("Data Mode", conf.mode)
    add_item("Pattern", conf.pattern)
    add_item("Rows num", conf.metadata.num_rows)
    add_item("Prescan", conf.metadata.prescan)
    add_item("Overscan", conf.metadata.overscan)
    add_item("Columns", conf.metadata.columns)


def new_image(new_tab, im, conf):
    raw = RawRepresentation(im)

    if conf.mode == 0:
        data = raw.get_matrix()
        add_image(new_tab.plot, data)
    elif conf.mode == 1:
        data = raw.get_avg()
        add_image(new_tab.plots[0], data[0])
        add_image(new_tab.plots[1], data[1])
        add_image(new_tab.plots[2], data[1] - data[0])
    elif conf.mode == 2:
        data = raw.get_light()
        add_image(new_tab.plots[0], data[0])
        add_image(new_tab.plots[1], data[1])
    elif conf.mode == 3:
        data = raw.get_bias()
        add_image(new_tab.plots[0], data[0])
        add_image(new_tab.plots[1], data[1])
    elif conf.mode == 4:
        plot = new_tab.plot.get_plot()
        # TODO: Make last and maxWidth configurable by the user¿?
        add_waveform(im, plot, 2048, True)


def add_image(plot, data, colormap="gray"):
    image = make.image(data, colormap=colormap)
    plot.get_plot().add_item(image)


def add_waveform(im, plot, max_width, last):
    curves = []
    reset_curves = []
    pixel_curves = []
    colors = [u'#aa00aa', u'#aaaa00', u'#00aaaa', u'#0000aa', u'#aa0000']
    for amp in im.amplifiers:
        if len(amp.rows) == 0:
            # TODO: Log it
            print("ERROR: No rows")
            continue

        row = amp.rows[0]
        row_num = row.meta['ccd_row_num']
        if max_width:
            if last:
                data = row.data[-max_width:]
            else:
                data = row.data[:min(len(row.data), max_width)]
        else:
            data = row.data
        x = range(len(data))
        y = [el & 0xffff for el in data]
        max_val = max(y)
        min_val = min(y)
        offset = min_val
        amplitude = max_val - min_val
        curve = make.curve(x, y, color=colors[amp.amp_id], linewidth=2.0)
        curve.setTitle("Amp {0} line {1}".format(amp.amp_id, row_num))
        curves.append(curve)

        y = [offset + amplitude * ((el & 0x10000) >> 16) for el in data]
        reset_params = CurveParam()
        reset_params.baseline = min_val
        reset_params.line.style = 'DotLine'
        reset_params.line.color = u'#aaaaff'
        reset_params.curvestyle = 'Sticks'
        reset_params.label = "Amp {0} line {1} - reset points".format(
            amp.amp_id, row_num)
        curve_reset = CurveItem(reset_params)
        curve_reset.set_data(x, y)
        reset_curves.append(curve_reset)

        y = [offset + amplitude * ((el & 0x20000) >> 17) for el in data]
        pixel_params = CurveParam()
        pixel_params.baseline = min_val
        pixel_params.line.style = 'DotLine'
        pixel_params.line.color = u'#aaffaa'
        pixel_params.curvestyle = 'Sticks'
        pixel_params.label = "Amp {0} line {1} - pixel points".format(
            amp.amp_id, row_num)
        curve_pixel = CurveItem(pixel_params)
        curve_pixel.set_data(x, y)
        # curve_pixel = make.curve(x, y)
        # curve_pixel.setTitle("Amp {0} line {1} - pixel points".format(amp.amp_id, row_num))
        pixel_curves.append(curve_pixel)

    # plot.add_item(make.legend("TR"))
    for curve_reset in reset_curves:
        plot.add_item(curve_reset)
    for curve_pixel in pixel_curves:
        plot.add_item(curve_pixel)
    for curve in curves:
        plot.add_item(curve)


def memory_usage():
    """Memory usage of the current process in kilobytes."""
    status = None
    result = "Memory Used NA"
    try:
        with open('/proc/self/status') as status:
            for line in status:
                parts = line.split()
                if parts:
                    key = parts[0][:-1]
                    if key == "VmRSS":
                        result = "{} MB".format(round(int(parts[1]) / 1024, 2))
    except:
        pass
    return result
