import argparse
import asyncio

from ruamel import yaml

from subscriber import Subscriber


async def main():
    _parser = argparse.ArgumentParser(prog='Subscriber')
    _parser.add_argument(
        'execution_id',
        action='extend',
        type=int,
        nargs='+',
    )
    _parser.add_argument(
        '-c', '--config',
        type=argparse.FileType('r', encoding='UTF-8'),
        default=open('config.yml', 'r', encoding='UTF-8'),
        help='specify a config file',
    )
    _args = _parser.parse_args()

    # 读取配置文件.
    _config: dict = yaml.safe_load(_args.config)
    _args.config.close()

    _subscriber = Subscriber(**_config)
    for _execution_id in _args.execution_id:
        await _subscriber.start(_execution_id)


if __name__ == '__main__':
    asyncio.run(main())
