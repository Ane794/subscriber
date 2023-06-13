from subscriber import Execution, TaskRunner


class WebsiteTask(TaskRunner):
    """ 示例任务 """

    _BASE_URL = 'https://google.com/'

    def __init__(self, execution: Execution, log_kwargs: dict, request_kwargs: dict):
        _log_kwargs = log_kwargs.copy()
        _log_kwargs.update(
            titles=[
                execution.account.website.name,
                execution.account.name,
                execution.task.name,
            ],
        )

        super().__init__(
            execution,
            log_kwargs=_log_kwargs,
            request_kwargs=request_kwargs.copy(),
        )

    def run(self) -> tuple[int, str]:
        """ 任务主要流程. """

        _res = self._get(WebsiteTask._BASE_URL)

        if _res.status_code != 200:
            self._err(_res.text)
        else:
            self._info(_res.text)

        return _res.status_code, _res.text
