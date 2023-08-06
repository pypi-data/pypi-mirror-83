import logging
import utility.utils as utils

################################################################################

class logger():
    def __init__(self, logfilename, logconsole = True, appname = "", level = "info"):
        utils.check_path_exists(logfilename)
        self.is_print = False

        if len(appname) <= 0: appname = __name__
        self.logger = logging.getLogger(appname)
        self.handler = logging.FileHandler(logfilename)
        self.handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.handler)
        if (logconsole):
            self.logger.addHandler(logging.StreamHandler())
        self.set_level(level = level)

    def set_level(self, level = "info"):
        if (level.upper() == "DEBUG"):
            self.set_debug_level()
        if (level.upper() == "INFO"):
            self.set_info_level()
        if (level.upper() == "WARNING"):
            self.set_warning_level()
        if (level.upper() == "ERROR"):
            self.set_error_level()
        if (level.upper() == "CRITICAL"):
            self.set_critical_level()

    ####################################################

    def set_debug_level(self):
        self.logger.setLevel(level = logging.DEBUG)

    def set_info_level(self):
        self.logger.setLevel(level = logging.INFO)

    def set_warning_level(self):
        self.logger.setLevel(level = logging.WARNING)

    def set_error_level(self):
        self.logger.setLevel(level = logging.ERROR)

    def set_critical_level(self):
        self.logger.setLevel(level = logging.CRITICAL)

    ####################################################

    def output(self, log, level = "info"):
        if (level.upper() == "DEBUG"):
            self.debug(log)
        if (level.upper() == "INFO"):
            self.info(log)
        if (level.upper() == "WARNING"):
            self.warning(log)
        if (level.upper() == "ERROR"):
            self.error(log)
        if (level.upper() == "CRITICAL"):
            self.critical(log)

    ####################################################

    def debug(self, log):
        if (self.is_print): print(log)
        self.logger.debug(log)

    def info(self, log):
        if (self.is_print): print(log)
        self.logger.info(log)

    def warning(self, log):
        if (self.is_print): print(log)
        self.logger.warning(log)

    def error(self, log):
        if (self.is_print): print(log)
        self.logger.error(log)

    def critical(self, log):
        if (self.is_print): print(log)
        self.logger.critical(log)
