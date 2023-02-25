import argparse

from ruamel.yaml import YAML, CommentedMap, CommentedSeq

from subscriber import Subscriber


def parse_yaml(obj):
    _result = dict(obj) if isinstance(obj, CommentedMap) \
        else list(obj) if isinstance(obj, CommentedSeq) \
        else obj

    for _ in _result if isinstance(_result, dict) \
            else range(0, len(_result)) if isinstance(_result, list) \
            else {}:
        _result[_] = parse_yaml(_result[_])

    return _result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Subscriber')
    parser.add_argument(
        'work_id',
        action='extend',
        type=int,
        nargs='+',
    )
    parser.add_argument(
        '-c', '--config',
        type=argparse.FileType('r', encoding='UTF-8'),
        default=open('others/config.yml', 'r', encoding='UTF-8'),
        help='specify a config file',
    )
    args = parser.parse_args()

    # 读取配置文件.
    config = dict(parse_yaml(YAML().load(args.config)))
    args.config.close()

    subscriber = Subscriber(**config)
    for work_id in args.work_id:
        subscriber.start(work_id)
