from .sql_util import SqlUtil
from ...models import *


class SqlFetchUtil(SqlUtil):
    def fetch_for(self, object_class, object_name: str, object_id: int, attr_names: list[str] = None):
        _ATTR_NAMES = attr_names.copy() if attr_names is not None else []

        _data = self.res_to_dict(
            self.fetchone(f'''select * from {object_name} where id = {object_id}''')
        )

        if not _data:
            print(f'''找不到 ID 为 `{object_id}` 的 `{object_name}`!''')
            return None

        for _name in _ATTR_NAMES:
            _attr_obj = getattr(self, f'fetch_{_name}')(_data.get(f'{_name}_id'))
            if not _attr_obj:
                return None
            _data[_name] = _attr_obj

        return object_class(**_data)

    def fetch_website(self, website_id: int) -> Website | None:
        return self.fetch_for(Website, 'website', website_id)

    def fetch_task(self, task_id: int) -> Task | None:
        return self.fetch_for(Task, 'task', task_id, ['website'])

    def fetch_account(self, account_id: int) -> Account | None:
        return self.fetch_for(Account, 'account', account_id, ['website'])

    def fetch_execution(self, execution_id: int) -> Execution | None:
        return self.fetch_for(Execution, 'execution', execution_id, ['task', 'account'])

    def update_for(self, object_name: str, object_id: int, data: dict[str]):
        self.update(
            f'''update {object_name} set ''' +
            ', '.join([
                _k + '=' + (
                    str(_v) if isinstance(_v, int) else
                    '\'%s\'' % _v if isinstance(_v, str) else
                    '\'%s\'' % json.dumps(_v, ensure_ascii=False)
                )
                for _k, _v in data.items()
            ]) +
            f''' where id={object_id}''',
        )

    def update_execution(self, execution_id: int, **data):
        self.update_for('execution', execution_id, data)
