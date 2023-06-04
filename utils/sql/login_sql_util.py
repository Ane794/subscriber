from models import *
from .sql_util import SqlUtil


class LoginSqlUtil(SqlUtil):
    def fetch_website(self, website_id: int) -> Website:
        _data = self.res_to_dict(
            self.fetchone(f'select * from website where id = {website_id}')
        )

        if not _data:
            print(f'找不到 website_id 为 {website_id} 的网站!')

        return Website(**_data)

    def fetch_account(self, account_id: int) -> Account:
        _data = self.res_to_dict(
            self.fetchone(f'select * from account where id = {account_id}')
        )

        _data.update(website=self.fetch_website(_data.get('website_id')))

        if _data is None:
            print(f'找不到 account_id 为 {account_id} 的账号!')
        return Account(**_data)

    def fetch_work(self, work_id: int) -> Work:
        _data = self.res_to_dict(
            self.fetchone(f'select * from work where id = {work_id}')
        )

        _data.update(account=self.fetch_account(_data.get('account_id')))

        if not _data:
            print(f'找不到 work_id 为 {work_id} 的网站!')

        return Work(**_data)
