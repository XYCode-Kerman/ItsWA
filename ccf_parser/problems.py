import decimal
import pathlib
from typing import Any, List, Literal, Optional

from pydantic import BaseModel, model_validator

# 比较器
Comparator = Literal[
    # 全文比较    全文比较，去除首尾空行（不是每行）
    'full', 'full_strip',
    # 逐行比较    逐行比较，去除首尾空格（每行）
    'line', 'line_strip',
    # 实数比较，与标准值相差小于10^-3
    'decimal_3'
]


class CheckPoint(BaseModel):
    input: str
    answer: str
    ckpt_score: int = 10

    input_type: Literal['STDIN', 'FILE']
    output_type: Literal['STDOUT', 'FILE']

    # 仅 input_type == FILE 时设置
    input_file: Optional[pathlib.Path] = None
    # 仅 output_type == FILE 时设置
    output_file: Optional[pathlib.Path] = None

    comparator: Comparator = 'line_strip'

    @model_validator(mode='after')
    def check_if_of(self):
        if self.input_type == 'STDIN':
            self.input_file = None

        if self.output_type == 'STDOUT':
            self.output_file = None

        return self

    def compare(self, output: str) -> bool:
        # CRLF转换到LF
        self.answer = self.answer.replace('\r\n', '\n')
        output = output.replace('\r\n', '\n')

        if self.comparator == 'full':
            return self.answer == output
        elif self.comparator == 'full_strip':
            return self.answer.strip() == output.strip()
        elif self.comparator == 'line':
            return self.answer.splitlines() == output.splitlines()
        elif self.comparator == 'line_strip':
            temp = [
                ans.strip() == out.strip()
                for ans, out in zip(self.answer.splitlines(), output.splitlines())
            ]

            ret = temp[0]
            for i in temp:
                ret &= i

            return ret
        elif self.comparator == 'decimal_3':
            try:
                return (decimal.Decimal(self.answer) - decimal.Decimal(output)).copy_abs() < 10**-3
            except decimal.InvalidOperation:
                return False


class JudgeConfig(BaseModel):
    # 不带后缀
    source_file_name: str
    languages: List[Literal['CPP', 'C']] = ['CPP']
    checkpoints: List[CheckPoint]


class Problem(BaseModel):
    name: str
    background: Optional[str] = '此题无题目背景'  # 题目背景
    description: str
    input_format: str
    output_format: str
    judge_config: JudgeConfig
