import pathlib
from typing import List, Literal

from pydantic import BaseModel

from ccf_parser.problems import Problem


class CCFHeader(BaseModel):
    name: str
    path: pathlib.Path
    description: str
    contest_type: Literal['OI', 'IOI']
    enable_oj: bool


class Contest(BaseModel):
    problems: List[Problem]
    languages: List[Literal['CPP', 'C']]


class CCF(BaseModel):
    header: CCFHeader
    contest: Contest
