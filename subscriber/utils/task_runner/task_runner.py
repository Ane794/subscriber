from .request_util import RequestUtil, RequestAsyncUtil
from ... import Subscriber
from ...models import Execution


class TaskRunner(RequestUtil):
    def __init__(self, execution: Execution, subscriber: Subscriber = None, log_kwargs=None, request_kwargs=None):
        """
        :param execution: 执行实例
        :param log_kwargs: `LogUtil` 的关键字参数
        :param request_kwargs: 发送请求所使用的关键字参数
        """
        self._subscriber: Subscriber = subscriber
        """ Subscriber 实例 """

        self._website = execution.task.website
        """ 网站实例 """
        self._account = execution.account
        """ 账号实例 """
        self._task = execution.task
        """ 任务实例 """
        self._execution = execution
        """ 执行实例 """

        _log_kwargs = log_kwargs.copy() if log_kwargs is not None else {}
        _request_kwargs = request_kwargs.copy() if request_kwargs is not None else {}

        _parsed_kwargs = self._parse_kwargs()
        for _ in _parsed_kwargs:
            _request_kwargs.setdefault(_, _parsed_kwargs.get(_))

        _log_kwargs.setdefault(
            'debug',
            self._execution.options.get('debug') or
            self._task.options.get('debug') or
            self._account.options.get('debug') or
            self._website.options.get('debug'),
        )
        _log_kwargs.setdefault('titles', [
            self._website.name,
            self._account.nickname if self._account.nickname else self._account.name,
            self._task.name,
        ])

        super().__init__(log_kwargs=_log_kwargs, request_kwargs=_request_kwargs)

    def start(self, *args, **kwargs) -> tuple[int, object]:
        """ 执行任务. """
        return self._start(self.run, args, kwargs)

    def run(self, *args, **kwargs) -> tuple[int, object]:
        """ 任务流程. """
        pass

    def _parse_kwargs(self) -> dict[str]:
        """
        从网站实例, 任务实例, 账号实例和执行实例中获取 Requests 参数.
        :return: Requests 参数
        """
        _kwargs = {}

        _KEYS = ['proxies']
        for _ in _KEYS:
            _VALUE = self._execution.options.get(
                _, self._account.options.get(
                    _, self._task.options.get(
                        _, self._website.options.get(_),
                    ),
                ),
            )
            if _VALUE is not None:
                _kwargs[_] = _VALUE

        _KEYS = ['User-Agent']
        _headers = self._website.options.get('headers', {})
        _ACCOUNT_HEADERS = self._account.options.get('headers')
        _TASK_HEADERS = self._task.options.get('headers')
        _EXECUTION_HEADERS = self._execution.options.get('headers')
        if _ACCOUNT_HEADERS:
            _headers.update(**_ACCOUNT_HEADERS)
        if _TASK_HEADERS:
            _headers.update(**_TASK_HEADERS)
        if _EXECUTION_HEADERS:
            _headers.update(**_EXECUTION_HEADERS)
        for _ in _KEYS:
            _VALUE = self._execution.options.get(
                _.lower(), self._account.options.get(
                    _.lower(), self._task.options.get(
                        _.lower(), self._website.options.get(_.lower()),
                    ),
                ),
            )
            if _VALUE:
                _headers[_] = _VALUE
        if _headers:
            _kwargs.update(headers=_headers)

        if isinstance(self._account.login_key, dict):
            _kwargs.update(cookies=self._account.login_key)

        return _kwargs


class TaskAsyncRunner(TaskRunner, RequestAsyncUtil):
    """ JobUtil 的异步版本 """

    async def start(self, *args, **kwargs) -> tuple[int, object]:
        """ 执行任务. """
        return await self._start(self.run, args, kwargs)

    async def run(self, *args, **kwargs) -> tuple[int, object]:
        pass
