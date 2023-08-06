#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import sys
import traceback

# Workarond for debian based systems
import os; os.environ.setdefault("QT_API", "pyqt5")

import coloredlogs
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication

from pyqt_tools import messages

from .config.config import get_valid_config
from .god import GOD

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-log-level', '-l', dest='loglevel', metavar='INFO', default='INFO', help='log level')
    args = parser.parse_args()

    coloredlogs.install(level=args.loglevel,
                        fmt='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s')

    try:
        QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        app = QApplication(sys.argv)

        cfg = get_valid_config()
        god = GOD(cfg)
        god.show_main_window()
        ret = app.exec_()
        god.close()
        sys.exit(ret)
    except Exception as ex:
        traceback.print_tb(ex)
        msg = "Can not run client: {}".format(ex)
        messages.show_fatal(msg, "Error during startup")

if __name__ == "__main__":
    main()
