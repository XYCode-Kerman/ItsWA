from typing import Dict, List

from pydantic import BaseModel, computed_field

from ccf_parser.status import Status

from .problems import CheckPoint


class CheckPointResult(BaseModel):
    ckpt: CheckPoint
    score: int
    status: Status
    output: str
    time: float = 0
    memory: float = 0


class JudgingResult(BaseModel):
    player_order: str
    problems_result: Dict[str, List[CheckPointResult]]  # key: Problem.name

    @computed_field  # type: ignore
    @property
    def sum_score(self) -> int:
        score: int = 0

        for problem_result in self.problems_result.values():
            for ckpt in problem_result:
                score += ckpt.score

        return score
