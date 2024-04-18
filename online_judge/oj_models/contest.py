from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import *
from uuid import UUID, uuid5

from pydantic import BaseModel, computed_field

import ccf_parser
from ccf_parser import CCF

ITSWA_OJ_PROBLEM_NAMESPACE = UUID('3a438ef7-a46d-4c85-af4d-45cbad5af9f3')


class OJContest(BaseModel):
    """有别于 ccf_parser 中的 Contest，更加详细的比赛信息需要从 ccf_parser 中获取"""
    contest_id: UUID
    ccf_file: Path

    start_time: datetime
    end_time: datetime

    @property
    def read_ccf(self) -> CCF:
        data = self.ccf_file.read_text('utf-8')
        return CCF.model_validate_json(data)

    @computed_field
    @property
    def name(self) -> str:
        return self.read_ccf.header.name

    @computed_field
    @property
    def description(self) -> str:
        return self.read_ccf.header.description


class OJProblem(BaseModel):
    """有别于 ccf_parser 中的 Problem，更加详细的题目信息需要从 ccf_parser 中获取"""

    name: str
    background: Optional[str] = '此题无题目背景'  # 题目背景
    description: str
    input_format: str
    output_format: str
    source_file_name: str
    languages: List[Literal['CPP']] = ['CPP']

    @computed_field
    @property
    def problem_id(self) -> UUID:
        return uuid5(
            ITSWA_OJ_PROBLEM_NAMESPACE,
            self.source_file_name
        )

    @staticmethod
    def load_from_ccf_problem(problem: ccf_parser.Problem) -> OJProblem:
        return OJProblem(
            name=problem.name,
            background=problem.background,
            description=problem.description,
            input_format=problem.input_format,
            output_format=problem.output_format,
            source_file_name=problem.judge_config.source_file_name,
            languages=['CPP']  # TODO: 默认支持 C++ 语言，后续可以添加更多语言支持。
        )
