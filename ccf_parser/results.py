from typing import Dict, List

from pydantic import BaseModel

from ccf_parser.status import Status

from .problems import CheckPoint, Problem


class CheckPointResult(BaseModel):
    ckpt: CheckPoint
    score: int
    status: Status


class JudgingResult(BaseModel):
    player_order: str
    problems_result: Dict[str, List[CheckPointResult]]  # key: Problem.name
