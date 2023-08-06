import os

import confuse

def get_valid_config():
    temp = {
        "connection": {
            "server_ip": confuse.String(),
        },
        "geometry": {
            "storage_rows": int,
            "active_rows": int,
            "prescan": int,
            "overscan": int,
            "columns": int,
        },
        "expose": {
            "mode": int,
            "time": int,
            "fake_data": bool,
        },
        "post_expose": {
            "images_dir": confuse.Filename(),
        },
        "adc": {
            "auto_calibrate": bool,
            "delay": int,
        },
        "timings": {
            "hor": {
                "acq": int,
                "del": int,
                "overlap": int,
                "postrg": int,
                "prerg": int,
                "rg": int,
            },
        },
        "discharge": {
            "duration": int,
            "reset": bool,
            "pixel": bool,
            "auto_enable": bool,
        },
        "offsets": {
            # Will be the same on amplifiers
            "value": float,
            "spd": bool,
            "pwr": bool,
            "auto_enable": bool,
        },
        "pid": {
            "p": float,
            "i": float,
            "d": float,
            "max_duty": float,
            "min_integral_error": float,
            "max_integral_error": float,
        },
    }

    config = confuse.LazyConfig("gfagui", __name__)

    v = config.get(temp)
    return v

