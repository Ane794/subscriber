from models import Work
from utils import JobUtil


class Job(JobUtil):
    """ 示例任务 """

    _BASE_URL = 'https://google.com/'

    def __init__(self, work: Work, log_kwargs: dict, **kwargs):
        log_kwargs.update(
            titles=[
                work.account.website.name,
                work.account.nickname,
                work.name,
            ],
        )

        super().__init__(
            work,
            log_kwargs=log_kwargs,
            **kwargs,
        )

    def _job(self):
        """ 任务主要流程. """

        _res = self._get(Job._BASE_URL)

        if _res.status_code != 200:
            self._err(_res.text)
        else:
            self._log(_res.text)

        return _res.status_code, _res.text
