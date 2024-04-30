# 注意：该模块是用于 Online Judge 的！正常评测请勿使用！
import random
import tempfile
from pathlib import Path
from typing import *

from ccf_parser import CheckPoint, CheckPointResult, JudgingResult
from ccf_parser.status import Status

from .languages import Language
from .runtime import simple_runtime


def simple_judging(code: str, language: Language, checkpoints: List[CheckPoint]) -> Generator[CheckPointResult, None, List[CheckPointResult]]:
    results: List[CheckPointResult] = []

    source_file = Path(tempfile.mkstemp(suffix='.' + language.suffix)[1])
    source_file.write_text(code, 'utf-8')

    compiled_path = Path(f'/tmp/{random.randint(0, 10**9)}.bin')

    compile_result = language.compile(source_file, compiled_path)

    # 编译失败
    if compile_result is False or compiled_path.exists() is False:
        for ckpt in checkpoints:
            ckpt_result = CheckPointResult(
                ckpt=ckpt, score=0, status=Status.CompileError, output='')
            yield ckpt_result
            results.append(ckpt_result)
        return results

    # 评测
    for ckpt in checkpoints:
        output, running_time = simple_runtime(compiled_path, ckpt.input,
                                              ckpt.input_type, ckpt.input_file)
        ckpt_result: Optional[CheckPointResult] = None

        # 运行成功
        if isinstance(output, str):
            if ckpt.compare(output):
                ckpt_result = CheckPointResult(
                    ckpt=ckpt, score=ckpt.ckpt_score, status=Status.Accepted, output=output)
            else:
                ckpt_result = CheckPointResult(
                    ckpt=ckpt, score=0, status=Status.WrongAnswer, output=output)
        # 运行失败
        else:
            ckpt_result = CheckPointResult(
                ckpt=ckpt, score=0, status=output, output='')

        yield ckpt_result
        results.append(ckpt_result)

    return results
