import datetime
import json


def _parse_json(string: str):
    """ 若一个字符串是 JSON 字符串, 转换成 `dict` 或 `list`; 否则不转换.

    :param string:
    :return:
    """
    try:
        _RESULT = json.loads(string)
        if isinstance(_RESULT, (list, dict)):
            return _RESULT
    except json.JSONDecodeError:
        pass
    return string


class DbModel:
    def __init__(self, **kwargs):
        for _ in kwargs:
            _value = kwargs.get(_)
            if _value is None:
                continue
            if isinstance(_value, str):
                _value = _parse_json(_value)
            setattr(self, _, _value)


class Website(DbModel):
    def __init__(self, **kwargs):
        self.id: int = 0
        """ 网站 ID """
        self.name: str = ''
        """ 网站名称 """
        self.options: dict[str] = {}
        """ 网站选项 """

        super().__init__(**kwargs)


class Task(DbModel):
    def __init__(self, **kwargs):
        self.id: int = 0
        """ 任务 ID """
        self.name: str = ''
        """ 任务名称 """
        self.options: dict[str] = {}
        """ 任务选项 """
        self.codes: dict[str, list[int]] = {'success': [0], 'ignored': []}
        """ 表示成功或忽略的返回码 """
        self.website_id: int = 0
        """ 网站 ID """
        self.website: Website = None
        """ 网站实例 """

        super().__init__(**kwargs)


class Account(DbModel):
    def __init__(self, **kwargs):
        self.id: int = 0
        """ 账号 ID """
        self.name: str = ''
        """ 账号名称  """
        self.login_key: str | dict[str] = ''
        """ 登录密钥; 可能是密码 (str) 或 Cookies (dict) """
        self.nickname: str = ''
        """ 账号昵称 """
        self.options: dict[str] = {}
        """ 账号选项 """
        self.website_id: int = 0
        """ 网站 ID """
        self.website: Website = None
        """ 网站实例 """

        super().__init__(**kwargs)


class Execution(DbModel):
    def __init__(self, **kwargs):
        self.id: int = 0
        """ 执行 ID """
        self.options: dict[str] = {}
        """ 执行选项 """
        self.task_id: int = 0
        """ 任务 ID """
        self.task: Task = None
        """ 任务实例 """
        self.account_id: int = 0
        """ 账号 ID """
        self.account: Account = None
        """ 账号实例 """
        self.result: list[int, object] = [-1, None]
        """ 上次运行结果 """
        self.last_start: datetime.datetime = None
        """ 上次开始时间 """
        self.last_end: datetime.datetime = None
        """ 上次结束时间 """

        super().__init__(**kwargs)
