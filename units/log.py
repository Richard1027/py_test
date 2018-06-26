# --*-- coding:utf8 --*--

"""
日志类，重写日志方法，定义日志级别、格式等
"""

import os,time
import logging
from logging.handlers import TimedRotatingFileHandler
from units.config import Log_Path, Config


class Logger:

    def __init__(self, logger_name = "pps_test"):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        log_name = c.get('file_name') if c and c.get('file_name') else 'pps-api'
        log_time = time.strftime("%Y-%m-%d", time.localtime())
        self.log_file_name = os.path.join(Log_Path, log_name +"-"+ log_time +".log")
        self.back_up = c.get('backup') if c and c.get('backup') else 5
        self.console_level = c.get('console_level') if c and c.get('console_level') else 'WARNING'
        self.file_level = c.get('file_level') if c and c.get('file_level') else 'DEBUG'
        pattern = c.get('pattern') if c and c.get('pattern') else '%(asctime)s-%(name)s-%(levelname)-%(message)s'
        self.format = logging.Formatter(pattern)

    def get_logger(self):

        # 避免重复的日志文件
        if not self.logger.handlers:

            # 新增控制台日志实例
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.format)
            console_handler.setLevel(logging.WARNING)
            self.logger.addHandler(console_handler)

            # 新增文件日志实例
            file_handler = TimedRotatingFileHandler(filename=self.log_file_name,
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.back_up,
                                                    delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.format)
            file_handler.setLevel(logging.DEBUG)
            self.logger.addHandler(file_handler)

        return self.logger

    #定义写入日志方法

    def Debug(self, msg):
        self.logger.debug(msg)

    def Info(self, msg):
        self.logger.info(msg)

    def Warn(self, msg):
        self.logger.warning(msg)

    def Error(self, msg):
        self.logger.error(msg)
