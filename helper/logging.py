from config import config
from helper1.logstash_formatter import LogstashFormatterV1
import logging


class Log:
    FORMAT = LogstashFormatterV1()

    def __init__(self):
        self.error_handler = self.create_file_handler('error', 'ERROR')
        self.console_handler = self.create_console_handler()
        self.log_level = config.get('log', 'log_level')

    def create_file_handler(self, file_name, log_level=None):
        handle = logging.FileHandler('%s/%s.log' % (config.get('log', 'log_dir'), file_name))
        handle.setFormatter(self.FORMAT)
        handle.setLevel(log_level if log_level else self.log_level)
        return handle

    def create_console_handler(self):
        console = logging.StreamHandler()
        console.setFormatter(self.FORMAT)
        console.setLevel(logging.DEBUG)
        return console

    def create_logger(self, logger_name):
        l = logging.getLogger(logger_name)
        l.setLevel(config.get('log', 'log_level'))
        l.propagate = False
        l.addHandler(self.error_handler)
        l.addHandler(self.create_file_handler(logger_name))
        if config.getint('log', 'console'):
            l.addHandler(self.console_handler)
        return l

log = Log()
logger = log.create_logger('app')
request_logger = log.create_logger('request')
