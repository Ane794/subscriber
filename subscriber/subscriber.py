import importlib

from utils.sql.login_sql_util import LoginSqlUtil


class Subscriber:
    def __init__(self, **config):
        """
        :param config:
            log: 日志设置
                log_dir: 日志目录
            request: # request 设置
                proxies: 代理
                    http: HTTP 代理
                    https: HTTPS 代理
                headers: 头
                ...: 其他 request 参数
        """
        self._conf = config
        self._conf.setdefault('sql', {})
        self._conf.get('sql').setdefault('engine', 'sqlite3')
        self._conf.get('sql').setdefault('database', 'subscriber.sqlite')

        self._conf.setdefault('log', {})
        self._conf.get('log').setdefault('log_dir', 'logs')

        self._conf.setdefault('request', {})

        # 数据库连接配置
        _sql_conf = self._conf.get('sql', {})
        self._login_util = LoginSqlUtil(**_sql_conf)

    def start(self, work_id: int):
        _work = self._login_util.fetch_work(work_id)

        _work_module = importlib.import_module(f'websites.{_work.account.website.name}.{_work.name}')
        """ 任务模块; 根据执行方法和网站名定位到 """
        return _work_module.Job(
            _work,
            request_kwargs=self._conf.get('request'),
            log_kwargs=self._conf.get('log'),
        ).start()
