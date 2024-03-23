import abc
import re

from utils import judge_logger


class Filter(abc.ABC):
    def __init__(self) -> None:
        """用于在编译前过滤不良代码，需要提前使用预处理器进行处理，以防止通过宏定义等方式绕过"""
        super().__init__()

    @abc.abstractmethod
    def filter(self, code: str) -> bool:
        """通过：True    不通过：False"""


class CPPFilter(Filter):
    def __init__(self) -> None:
        super().__init__()

        self.regex_rules = [
            '#include<con>',
            '#include<\/dev\/.*>',
            'system\(.*\)',
            'popen\(.*\)'
        ]

    def filter(self, code: str) -> bool:
        for regex_rule in self.regex_rules:
            if re.match(regex_rule, code, re.IGNORECASE) is not None:
                judge_logger.debug(f'匹配到非法代码，规则 {regex_rule}。')
                return False
