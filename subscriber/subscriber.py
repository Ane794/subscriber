import asyncio
import datetime
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

    def start(
            self,
            execution_id: int,
            *args,
            websites_package: str = '',
            **kwargs,
    ) -> tuple[int, object]:
        _execution = self.get_execution(execution_id)
        if not websites_package:
            websites_package = self._conf.get('websites_package', 'websites')

        _website_task = self.init_website_task(websites_package, _execution)
        self._sql.update_execution(
            _execution.id,
            last_start=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )

        if asyncio.iscoroutinefunction(_website_task.start):  # 异步执行.
            _RES: tuple[int, object] = asyncio.run(_website_task.start(*args, **kwargs))
        else:  # 同步执行.
            _RES: tuple[int, object] = _website_task.start(*args, **kwargs)

        self._sql.update_execution(
            _execution.id,
            last_end=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            result=_RES,
        )

        return _RES

    def info(self, execution_id: int) -> dict[str]:
        _EXECUTION = self.get_execution(execution_id)
        return {
            'website': _EXECUTION.task.website.name,
            'task': _EXECUTION.task.name,
            'user': _EXECUTION.account.name,
            'nickname': _EXECUTION.account.nickname,
            'last_run': {
                'start_time': _EXECUTION.last_start.strftime('%Y-%m-%d %H:%M:%S')
                if _EXECUTION.last_start is not None else None,
                'end_time': _EXECUTION.last_end.strftime('%Y-%m-%d %H:%M:%S')
                if _EXECUTION.last_end is not None else None,
                'result': 'success' if _EXECUTION.result[0] in _EXECUTION.task.codes.get('success', []) else
                'ignored' if _EXECUTION.result[0] in _EXECUTION.task.codes.get('ignored', []) else
                'failure',
                'code': _EXECUTION.result[0],
                'data': _EXECUTION.result[1],
            },
        }

    def get_execution(self, execution_id):
        return self._sql.fetch_execution(execution_id)

    def init_website_task(self, websites_package, execution):
        _task_module = importlib.import_module(
            f'.{execution.account.website.name}.{execution.task.name}', websites_package
        )
        """ 任务执行模块; 根据网站名称和任务名称定位到 """

        return _task_module.WebsiteTask(
            execution,
            self,
            request_kwargs=self._conf.get('request'),
            log_kwargs=self._conf.get('log'),
        )
