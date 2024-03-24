import pathlib
import subprocess
from typing import Literal, Union

from utils import judge_logger

from .status import Status


def simple_runtime(executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN', 'FILE'], file_input_path: pathlib.Path = None, timeout: float = 1.0) -> Union[str, Status]:
    """返回 STDOUT（STDOUT 无输出时返回第一个后缀为 .out 的文件的内容）"""
    if file_input_path is not None:
        if file_input_path.is_absolute():
            judge_logger.warning(
                f'执行评测时的输入文件路径 {file_input_path} 是绝对路径，正确的格式应当为 `Path("hello.in")` 一类。\n运行失败，返回状态码 RE。')
            return Status.RuntimeError

    executeable_file.chmod(0o700)

    if input_type == 'STDIN':
        process = subprocess.Popen(
            executeable_file.absolute().__str__(),
            bufsize=-1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=executeable_file.parent
        )

        try:
            stdout, stderr = process.communicate(
                input_content.encode('utf-8'), timeout=timeout)
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return Status.TimeLimitExceeded

        if process.returncode != 0:
            return Status.RuntimeError

        return stdout.decode('utf-8')
    else:
        executeable_file.parent.joinpath(file_input_path).write_text(
            input_content, encoding='utf-8')

        process = subprocess.Popen(
            executeable_file.absolute().__str__(),
            bufsize=-1,
            cwd=executeable_file.parent
        )

        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            return Status.TimeLimitExceeded

        if process.returncode != 0:
            return Status.RuntimeError

        output_file = None
        for file in executeable_file.parent.iterdir():
            if file.suffix == '.out':
                output_file = file

        if output_file is None:
            return Status.RuntimeError  # pragma: no cover
        return output_file.read_text(encoding='utf-8')
