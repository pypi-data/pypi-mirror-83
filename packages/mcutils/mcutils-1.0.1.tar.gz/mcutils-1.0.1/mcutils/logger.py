import datetime

from .print_manager import *


class LogSettings:
    display_logs = False


class Log:
    def __init__(self, text, is_error=False):
        self.time_stamp = datetime.datetime.now()
        self.text = text
        self.is_error = is_error

    def get_text_log(self):
        return "{} => <{}>".format(self.time_stamp, self.text)

    def print_log(self):
        if LogSettings.display_logs:
            text = self.get_text_log()
            if self.is_error:
                mcprint(text=text, color=Color.RED)
            else:
                mcprint(text=text, color=Color.YELLOW)
            return text


class LogManager:

    def __init__(self, developer_mode=False):
        self.logs = []
        self.developer_mode = developer_mode

    def log(self, text, is_error=False):
        log = Log(text, is_error)
        self.logs.append(log)

        if self.developer_mode:
            log.print_log()

    def print_logs(self):
        for log in self.logs:
            log.print_log()

    def clear_logs(self):
        self.logs.clear()

    def write_logs(self, path='logs.txt'):
        with open(path, 'w') as log_file:
            for log in self.logs:
                log_file.write(log.get_text_log() + "\n")
