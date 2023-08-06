import csv
from time import strftime
from os import makedirs

from appdirs import AppDirs

app_dirs = AppDirs("gfagui")
makedirs(app_dirs.user_cache_dir, exist_ok=True)


class _BaseDataLog:

    def __init__(self, dir_name, header: list):
        self._dir = "{}/{}".format(app_dirs.user_cache_dir, dir_name)
        makedirs(self._dir, exist_ok=True)
        self._header = ["TIMESTAMP"] + header
        self.file = None

    def _create_file(self):
        timestamp = strftime("%y%m%d%H%M%S")
        file_name = "{}/{}.csv".format(self._dir, timestamp)
        self.file = open(file_name, "w", encoding="utf-8")

        file_info = "# Created on {}\n".format(timestamp)
        self.file.write(file_info)
        self._log_file = csv.writer(self.file)

        self._log_file.writerow(self._header)

    def add_row(self, row):
        if self.file is None:
            self._create_file()
        timestamp = strftime("%y%m%d%H%M%S")
        self._log_file.writerow([timestamp] + row)
        self.file.flush()

    def close(self):
        if self.file is not None:
            self.file.close()


class PIDDataLog(_BaseDataLog):

    def __init__(self):
        super(PIDDataLog, self).__init__("pid", ["COLD", "HOT", "OUTPUT(%)"])


class ExposureDataLog(_BaseDataLog):

    def __init__(self):
        super(ExposureDataLog, self).__init__("expose", ["ELAPSED_EXPOSE_TIME"])

    def add_row(self, elapsed_time: float):
        super().add_row([elapsed_time])

