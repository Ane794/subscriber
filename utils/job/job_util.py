import aiohttp

from models import Work
from .request_util import RequestUtil, RequestAsyncUtil


class JobUtil(RequestUtil):
    """ 任务基类 """

    def __init__(self, work: Work, request_kwargs=None, log_kwargs=None):
        """
        :param work: 任务实例
        :param request_kwargs: Request 参数; 将依次根据任务选项, 账号选项, 网站选项覆盖后用以初始化 RequestUtil
        :param log_kwargs: 日志参数; 用以初始化 LogUtil
        """
        self._website = work.account.website
        """ 网站实例 """
        self._account = work.account
        """ 账号实例 """
        self._work = work
        """ 任务实例 """

        if request_kwargs is None:
            request_kwargs = {}
        if log_kwargs is None:
            log_kwargs = {}

        _parsed_kwargs = self._parse_kwargs()
        for _ in _parsed_kwargs:
            request_kwargs.setdefault(_, _parsed_kwargs.get(_))

        log_kwargs.setdefault('debug', self._website.options.get('debug', False))
        log_kwargs.setdefault('titles', [
            self._website.name,
            self._account.nickname if self._account.nickname else self._account.name,
            work.name,
        ])

        super().__init__(
            log_kwargs=log_kwargs,
            **request_kwargs,
        )

    def start(self, title: str = '作业') -> (int, object):
        """ 执行作业. """
        return self._start(self._job, title)

    def _start(self, job, title='') -> (int, object):
        return super()._start(job, title)

    def _job(self) -> (int, object):
        """ 作业. """
        pass

    def _parse_kwargs(self) -> dict:
        """ 从网站实例, 账号实例和任务实例中获取 Requests 参数.

        :return: Requests 参数
        """
        _kwargs = {}

        _keys = ['proxies']
        for _ in _keys:
            _value = self._work.options.get(
                _, self._account.options.get(
                    _, self._website.options.get(_)
                )
            )
            if _value is not None:
                _kwargs[_] = _value

        _keys = ['User-Agent']
        _headers = self._website.options.get('headers', {})
        _account_headers = self._account.options.get('headers')
        _work_headers = self._account.options.get('headers')
        if _account_headers:
            _headers.update(**_account_headers)
        if _work_headers:
            _headers.update(**_work_headers)
        for _ in _keys:
            _value = self._work.options.get(
                _.lower(), self._account.options.get(
                    _.lower(), self._website.options.get(_.lower())
                )
            )
            if _value:
                _headers[_] = _value
        if _headers:
            _kwargs.update(headers=_headers)

        if isinstance(self._account.login_key, dict):
            _kwargs.update(cookies=self._account.login_key)

        return _kwargs


class JobAsyncUtil(JobUtil, RequestAsyncUtil):
    """ JobUtil 的异步版本 """

    def _run(self, job) -> (int, object):
        self._session = aiohttp.ClientSession(cookies=self._account.login_key)
        return self._loop.run_until_complete(job())

    async def _job(self) -> (int, object):
        pass

    def _end(self):
        self._loop.run_until_complete(self._session.close())
