import asyncio
import json

import aiohttp
import requests

from .log_util import LogUtil


class RequestUtil(LogUtil):
    class UnexpectedStatusCodeError(Exception):
        """ 因状态码与预期不符产生的异常. """

        def __init__(self, expected_code: int, status_code: int):
            self.expected_code = expected_code
            self.status_code = status_code
            self.msg = f'响应的状态码 ({self.status_code}) 与预期 ({self.expected_code}) 不符!'

        def __str__(self):
            return self.msg

    def __init__(self, log_kwargs: dict = None, request_kwargs: dict = None):
        """
        :param log_kwargs: `LogUtil` 的关键字参数
        :param request_kwargs: 发送请求所使用的关键字参数
        """
        if log_kwargs is None:
            log_kwargs = {}
        if request_kwargs is None:
            request_kwargs = {}

        super().__init__(**log_kwargs)

        self._request_kwargs = request_kwargs
        """ 请求参数 """
        self._session = None
        """ 会话 """
        self.failed = False
        """ 上次执行是否失败 """

    def __bool__(self):
        """ 上次执行是否失败. """
        return self.failed

    def _start(self, fun, args: tuple, kwargs: dict[str]):
        """ 调用方法 `self._run(fun)` 并捕获异常和返回值; 失败时自动重试. """
        try:
            result = self._run(fun, args, kwargs)
            self.failed = False
            return result
        except Exception as e:
            self.failed = True
            self._err(e)
        finally:
            self._end()

    def _run(self, fun, args: tuple, kwargs: dict[str]):
        """
        准备运行时的环境 (如新建会话等); 执行函数 `fun()`.
        :param fun: 待执行的函数
        :return: fun() 的返回值
        """
        self._session = requests.Session()
        return fun(*args, **kwargs)

    def _end(self):
        """ 清理运行时的环境 (如关闭会话, 清除缓存等). """
        self._session.close()

    def _request(self, *args, expected_code=None, outputs_res_body=False, **kwargs) -> requests.Response:
        """
        封装 `request()` 方法, 输出相关信息到终端和日志.
        :param expected_code: 期望得到的状态码
        :param outputs_res_body: 是否输出响应内容
        :return: `Response` 实例
        """
        _res = self._session.request(*args, **self._parse_request_kwargs(kwargs))

        if _res.request.body:
            self._debug(f'request body: {_res.request.body}')
        self._debug(f'response headers: {_res.headers}')
        if outputs_res_body or self._is_debug:
            self._debug(f'response content: {_res.text}')

        if expected_code is not None and _res.status_code != expected_code:
            raise self.UnexpectedStatusCodeError(expected_code, _res.status_code)

        return _res

    def _parse_request_kwargs(self, kwargs: dict[str]) -> dict[str]:
        """
        将新参数与 self._request_kwargs 合并.
        :param kwargs: 新的 Request 参数
        :return: 合并得到的 Request 参数
        """
        for _ in self._request_kwargs:
            if isinstance(kwargs.get(_), dict):
                kwargs.get(_).update(**self._request_kwargs.get(_))
            else:
                kwargs.setdefault(_, self._request_kwargs.get(_))

        return kwargs

    def _get(self, *args, **kwargs) -> requests.Response:
        return self._request('GET', *args, **kwargs)

    def _post(self, *args, **kwargs) -> requests.Response:
        return self._request('POST', *args, **kwargs)

    def _put(self, *args, **kwargs) -> requests.Response:
        return self._request('PUT', *args, **kwargs)


class RequestAsyncUtil(RequestUtil):
    """ `RequestUtil` 的异步版本 """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._loop = asyncio.get_event_loop()
        self._session: aiohttp.ClientSession

    async def _start(self, fun, args: tuple, kwargs: dict[str]):
        """ 调用方法 `self._run(fun)` 并捕获异常和返回值; 失败时自动重试. """
        try:
            result = await self._run(fun, args, kwargs)
            self.failed = False
            return result
        except Exception as e:
            self.failed = True
            self._err(e)
            return 1, e
        finally:
            await self._end()

    async def _run(self, fun, args: tuple, kwargs: dict[str]):
        self._session = aiohttp.ClientSession()
        return await fun(*args, **kwargs)

    async def _end(self):
        await self._session.close()

    async def _request(self, *args, expected_code: int = None, outputs_res_body=False,
                       **kwargs) -> aiohttp.ClientResponse:
        _res = await self._session.request(*args, **self._parse_request_kwargs(kwargs))

        self._debug("response: " + str(_res).replace('\n', ''))
        if outputs_res_body:
            self._debug(f'response content: {json.loads(await _res.text())}')

        if expected_code is not None and _res.status != expected_code:
            raise self.UnexpectedStatusCodeError(expected_code, _res.status)

        return _res

    async def _get(self, *args, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('GET', *args, **kwargs)

    async def _post(self, *args, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('POST', *args, **kwargs)

    async def _put(self, *args, **kwargs) -> aiohttp.ClientResponse:
        return await self._request('PUT', *args, **kwargs)
