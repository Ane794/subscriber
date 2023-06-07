import json
import re


def _parse_json(string: str):
    """ 若一个字符串是 JSON 字符串, 递归转换成 dict 或 list; 否则不转换.

    :param string:
    :return:
    """
    if not (re.match("{.*}", string) or re.match("\\[.*]", string)):
        return string

    _obj = json.loads(string)

    for _ in _obj if type(_obj) is dict else range(0, len(_obj)):
        _value = _obj[_]
        if type(_value) is str:
            _obj[_] = _parse_json(_value)
    return _obj


class DbModel:
    def __init__(self, **kwargs):
        for _ in kwargs:
            value = kwargs.get(_)
            if value is None:
                continue
            if isinstance(value, str):
                value = _parse_json(value)
            self.__setattr__(_, value)


class Website(DbModel):
    def __init__(self, **kwargs):
        self.id = 0
        """ 网站 ID """
        self.name = ''
        """ 网站名称 """
        self.options = {}
        """ 网站选项 """

        super().__init__(**kwargs)


class Account(DbModel):
    def __init__(self, **kwargs):
        self.id = 0
        """ 账号 ID """
        self.name = ''
        """ 账号名称  """
        self.login_key = ''
        """ 登录密钥; 可能是密码 (str) 或 Cookies (dict) """
        self.nickname = ''
        """ 账号昵称 """
        self.options = {}
        """ 账号选项 """
        self.website_id = 0
        """ 网站 ID """
        self.website = None
        """ 网站实例 """

        super().__init__(**kwargs)


class Work(DbModel):
    def __init__(self, **kwargs):
        self.id = 0
        """ 任务 ID """
        self.name = ''
        """ 任务名称 """
        self.options = {}
        """ 任务选项 """
        self.account_id = 0
        """ 账号 ID """
        self.account = None
        """ 账号实例 """

        super().__init__(**kwargs)
