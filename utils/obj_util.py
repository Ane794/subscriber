import json
import re


def parse_json(string: str):
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
            _obj[_] = parse_json(_value)
    return _obj
