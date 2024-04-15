from pathlib import Path

import pydantic
from fastapi import HTTPException

from ccf_parser import CCF


def require_ccf_file(ccf_file: Path) -> Path:
    if ccf_file.name != "ccf.json":
        raise HTTPException(status_code=400, detail="不是一个 CCF 文件")

    if not ccf_file.exists():
        raise HTTPException(status_code=404, detail="CCF 文件不存在")

    if not ccf_file.is_file():
        raise HTTPException(status_code=400, detail="不是一个有效的文件")

    try:
        ccf = CCF.model_validate_json(ccf_file.read_text('utf-8'))
    except pydantic.ValidationError as e:
        raise HTTPException(
            status_code=400, detail=f"CCF 文件格式错误: {e.errors()}")

    return ccf_file
