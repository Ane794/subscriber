import argparse

from ruamel import yaml

from subscriber import Subscriber

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
        default=open('config.yml', 'r', encoding='UTF-8'),
        help='specify a config file',
    )
    args = parser.parse_args()

    # 读取配置文件.
    config: dict = yaml.safe_load(args.config)
    args.config.close()

    subscriber = Subscriber(**config)
    for work_id in args.work_id:
        subscriber.start(work_id)