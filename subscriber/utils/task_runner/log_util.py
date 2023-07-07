import logging
import os

import sys
import traceback


class LogUtil:
    def __init__(self, titles: list[str], log_dir: str, debug: bool = False):
        """
        :param titles: 标题列表
        :param log_dir: 日志根目录
        :param debug: 是否在 debug; `False` 时将跳过 `_debug()` 的控制台输出
        """
        self._TITLES: list[str] = titles.copy()
        """ 标题列表 """
        self._LOG_DIR: str = log_dir
        """ 日志根目录 """
        self._IS_DEBUG: bool = debug
        """ 是否在 debug; False 时将跳过方法 LogUtil._debug() """

        self._refresh_logging_config()

    @staticmethod
    def _make_log_dir(dirs: list[str]):
        """
        创建日志目录.
        :param dirs: 目录列表; 按从外层到内层的顺序依次列出
        """
        _path = '/'.join(dirs)
        os.makedirs(_path, exist_ok=True)

    def _refresh_logging_config(self):
        """ 刷新日志设置. """
        _DIRS: list[dir] = [self._LOG_DIR] + self._TITLES
        """ 目录列表; 按从外层到内层的顺序依次列出 """

        self._make_log_dir(_DIRS)

        # 刷新日志格式.
        logging.basicConfig(
            handlers=[
                logging.FileHandler(
                    filename='%s.log' % ('/'.join(_DIRS)), mode='a', encoding='UTF-8',
                ),
            ],
            format='%(asctime)s  %(levelname)-8s'
                   f' [{"][".join(self._TITLES)}]'
                   ' %(message)s',
            level=logging.DEBUG,
        )

    def _log(self, level: int, msg='', prints: bool = True, file=sys.stdout):
        """
        将消息格式化后输出到日志和终端.
        :param level: 日志等级
        :param msg: 信息
        :param prints: 是否输出到终端
        :param file: 函数 `print` 的 `file` 参数
        """
        if prints:
            print(
                '%-8s [%s] %s' % (
                    logging.getLevelName(level),
                    ']['.join(self._TITLES),
                    msg
                ),
                file=file,
            )
        logging.log(level, msg)

    def _debug(self, msg):
        self._log(logging.DEBUG, msg, self._IS_DEBUG)

    def _info(self, msg):
        self._log(logging.INFO, msg)

    def _warn(self, msg):
        self._log(logging.WARNING, msg)

    def _err(self, msg):
        self._log(logging.ERROR, msg, file=sys.stderr)

    def _exception(self, exc):
        self._err(''.join(traceback.format_exception(exc)))
