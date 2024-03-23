import pathlib
from typing import List, Literal, Optional

from pydantic import BaseModel


class CheckPoint(BaseModel):
    input: str
    answer: str

    input_type: Literal['STDIN', 'FILE']
    output_type: Literal['STDOUT', 'FILE']

    # 仅 input_type == FILE 时设置
    input_file: Optional[pathlib.Path] = None
    # 仅 output_type == FILE 时设置
    output_file: Optional[pathlib.Path] = None

    def compare(self, output: str) -> bool:
        return self.answer.strip() == output.strip()


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
