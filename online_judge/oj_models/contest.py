from datetime import datetime
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel

from ccf_parser import CCF


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
