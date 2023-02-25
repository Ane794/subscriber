import logging
import os


class LogUtil:
    """ 日志输出目录 """

    def __init__(self, titles: list, log_dir: str, debug: bool = False):
        """
        :param titles: 标题
        :param debug: 是否在 debug; False 时将跳过方法 LogUtil._debug()
        """
        self._titles = titles
        self._log_dir = log_dir
        self._is_debug = debug
        """ 是否在 debug; False 时将跳过方法 LogUtil._debug() """

        self._refresh_logging_config()

    @staticmethod
    def _make_log_dir(dirs):
        for _ in range(len(dirs) - 1):
            _path = '/'.join(dirs[:_ + 1])
            if not os.path.exists(_path):
                os.mkdir(_path)

    def _refresh_logging_config(self):
        _dirs = [self._log_dir] + self._titles

        self._make_log_dir(_dirs)

        """ 刷新日志格式. """
        logging.basicConfig(
            handlers=[
                logging.FileHandler(
                    filename='%s.log' % ('/'.join(_dirs)), mode='a', encoding='UTF-8',
                )
            ],
            format='%(asctime)s  %(levelname)-8s'
                   f' [{"][".join(self._titles)}]'
                   ' %(message)s',
            level=logging.DEBUG,
        )

    def _log(self, level, msg=''):
        """ 将消息格式化后输出到日志和终端.

        :param level: 日志等级
        :param msg: 信息
        """
        print('%-8s [%s] %s' % (
            logging.getLevelName(level),
            ']['.join(self._titles),
            msg
        ))
        logging.log(level, msg)

    def _debug(self, msg):
        if not self._is_debug:
            return
        self._log(logging.DEBUG, msg)

    def _info(self, msg):
        self._log(logging.INFO, msg)

    def _warn(self, msg):
        self._log(logging.WARNING, msg)

    def _err(self, msg):
        self._log(logging.ERROR, msg)

    def _exception(self, msg):
        self._err(msg)
