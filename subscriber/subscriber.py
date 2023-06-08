import asyncio
import importlib

from .utils.sql import SqlFetchUtil


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
        self._conf: dict = config
        self._sql: SqlFetchUtil

        self._init_conf()

    def _init_conf(self):
        self._conf.setdefault('sql', {})
        self._conf.get('sql').setdefault('engine', 'sqlite3')
        self._conf.get('sql').setdefault('database', 'subscriber.sqlite')

        self._conf.setdefault('log', {})
        self._conf.get('log').setdefault('log_dir', 'logs')

        self._conf.setdefault('request', {})

        # 数据库连接配置
        _sql_conf = self._conf.get('sql', {})
        self._sql = SqlFetchUtil(**_sql_conf)

    def start(self, websites_package, execution_id: int) -> tuple[int, object]:
        _execution = self._sql.fetch_execution(execution_id)

        _task_module = importlib.import_module(
            f'.{_execution.account.website.name}.{_execution.task.name}', websites_package
        )
        """ 任务执行模块; 根据网站名称和任务名称定位到 """

        _website_task = _task_module.WebsiteTask(
            _execution,
            request_kwargs=self._conf.get('request'),
            log_kwargs=self._conf.get('log'),
        )

        if asyncio.iscoroutinefunction(_website_task.start):  # 异步执行.
            return asyncio.run(_website_task.start())
        else:  # 同步执行.
            return _website_task.start()
