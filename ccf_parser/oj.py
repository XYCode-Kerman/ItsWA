from datetime import datetime

from pydantic import BaseModel


class OJConfig(BaseModel):
    start_time: datetime
    end_time: datetime
