from .request_util import RequestUtil, RequestAsyncUtil
from ...models import Execution


class TaskRunner(RequestUtil):
    def __init__(self, execution: Execution, log_kwargs=None, request_kwargs=None):
        """
        :param execution: 执行实例
        :param log_kwargs: `LogUtil` 的关键字参数
        :param request_kwargs: 发送请求所使用的关键字参数
        """
        self._website = execution.task.website
        """ 网站实例 """
        self._account = execution.account
        """ 账号实例 """
        self._task = execution.task
        """ 任务实例 """
        self._execution = execution
        """ 执行实例 """

        if log_kwargs is None:
            log_kwargs = {}
        if request_kwargs is None:
            request_kwargs = {}

        _parsed_kwargs = self._parse_kwargs()
        for _ in _parsed_kwargs:
            request_kwargs.setdefault(_, _parsed_kwargs.get(_))

        log_kwargs.setdefault(
            'debug',
            self._execution.options.get('debug') or
            self._task.options.get('debug') or
            self._account.options.get('debug') or
            self._website.options.get('debug'),
        )
        log_kwargs.setdefault('titles', [
            self._website.name,
            self._account.nickname if self._account.nickname else self._account.name,
            self._task.name,
        ])

        super().__init__(log_kwargs=log_kwargs, request_kwargs=request_kwargs)

    def start(self) -> tuple[int, object]:
        """ 执行任务. """
        return self._start(self.run)

    def run(self) -> tuple[int, object]:
        """ 任务流程. """
        pass

    def _parse_kwargs(self) -> dict[str]:
        """
        从网站实例, 任务实例, 账号实例和执行实例中获取 Requests 参数.
        :return: Requests 参数
        """
        _kwargs = {}

        _keys = ['proxies']
        for _ in _keys:
            _value = self._execution.options.get(
                _, self._account.options.get(
                    _, self._task.options.get(
                        _, self._website.options.get(_),
                    ),
                ),
            )
            if _value is not None:
                _kwargs[_] = _value

        _keys = ['User-Agent']
        _headers = self._website.options.get('headers', {})
        _account_headers = self._account.options.get('headers')
        _task_headers = self._task.options.get('headers')
        _execution_headers = self._execution.options.get('headers')
        if _account_headers:
            _headers.update(**_account_headers)
        if _task_headers:
            _headers.update(**_task_headers)
        if _execution_headers:
            _headers.update(**_execution_headers)
        for _ in _keys:
            _value = self._execution.options.get(
                _.lower(), self._account.options.get(
                    _.lower(), self._task.options.get(
                        _.lower(), self._website.options.get(_.lower()),
                    ),
                ),
            )
            if _value:
                _headers[_] = _value
        if _headers:
            _kwargs.update(headers=_headers)

        if isinstance(self._account.login_key, dict):
            _kwargs.update(cookies=self._account.login_key)

        return _kwargs


class TaskAsyncRunner(TaskRunner, RequestAsyncUtil):
    """ JobUtil 的异步版本 """

    async def start(self) -> tuple[int, object]:
        """ 执行任务. """
        return await self._start(self.run)

    async def run(self) -> tuple[int, object]:
        pass
