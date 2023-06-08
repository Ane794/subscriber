from .sql_util import SqlUtil
from ...models import *


class SqlFetchUtil(SqlUtil):
    def fetch_for(self, object_class, object_name: str, object_id: int, attr_names: list[str] = None):
        if attr_names is None:
            attr_names = []

        _data = self.res_to_dict(
            self.fetchone(f'select * from {object_name} where id = {object_id}')
        )

        if not _data:
            print(f'找不到 ID 为 `{object_id}` 的 `{object_name}`!')
            return None

        for _name in attr_names:
            attr_obj = getattr(self, f'fetch_{_name}')(_data.get(f'{_name}_id'))
            if not attr_obj:
                return None
            _data[_name] = attr_obj

        return object_class(**_data)

    def fetch_website(self, website_id: int) -> Website | None:
        return self.fetch_for(Website, 'website', website_id)

    def fetch_task(self, task_id: int) -> Task | None:
        return self.fetch_for(Task, 'task', task_id, ['website'])

    def fetch_account(self, account_id: int) -> Account | None:
        return self.fetch_for(Account, 'account', account_id, ['website'])

    def fetch_execution(self, execution_id: int) -> Execution | None:
        return self.fetch_for(Execution, 'execution', execution_id, ['task', 'account'])
