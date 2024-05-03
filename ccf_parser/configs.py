import pathlib
from typing import List

from pydantic import BaseModel


class ContestIndex(BaseModel):
    name: str
    description: str
    ccf_file: pathlib.Path


ContestIndexList = List[ContestIndex]
