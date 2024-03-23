import logging

from rich.logging import RichHandler

logging.basicConfig(
    handlers=[RichHandler()],
    level=logging.DEBUG,
)

manager_logger = logging.getLogger('ItsWA-Manager')
judge_logger = logging.getLogger('ItsWA-Judge')
online_judge_logger = logging.getLogger('ItsWA-OnlineJudge')
