import os
import pathlib
import subprocess
import threading
from typing import Literal, Tuple, Union

import psutil
import psutil._common

from ccf_parser.status import Status
from utils import judge_logger


class SimpleRuntime(object):
    def __init__(self) -> None:
        pass

    def calling_precheck(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN', 'FILE'], file_input_path: pathlib.Path = None, timeout: float = 1.0) -> bool:
        if file_input_path is not None:
            if file_input_path.is_absolute():
                judge_logger.warning(
                    f'执行评测时的输入文件路径 {file_input_path} 是绝对路径，正确的格式应当为 `Path("hello.in")` 一类。\n运行失败，返回状态码 RE。')
                return False

        executeable_file.chmod(0o700)

    def __call__(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN', 'FILE'], file_input_path: pathlib.Path = None, timeout: float = 1.0) -> Tuple[Union[str, Status], float, float]:
        """返回 STDOUT（STDOUT 无输出时返回第一个后缀为 .out 的文件的内容）或Status(运行失败)，运行所用的CPU时间(s)，运行所用的内存（MiB）"""
        if self.calling_precheck(executeable_file, input_content, input_type, file_input_path, timeout) is False:
            return Status.RuntimeError, 0, 0

        # 监测数据
        process_cpu_time: psutil._common.pcputimes = psutil._common.pcputimes(
            user=-1, system=-1, children_user=-1, children_system=-1)  # 单位s
        max_process_rss: int = 0  # 单位 MiB
        signal = True

        # 监测器
        def _watcher():
            nonlocal process_cpu_time, signal, max_process_rss
            while signal and psutil_process.is_running():
                try:
                    process_cpu_time = psutil_process.cpu_times()
                    rss = psutil_process.memory_full_info().rss / 1048576

                    if rss > max_process_rss:
                        max_process_rss = rss
                except psutil.NoSuchProcess:
                    return

        # 运行
        process = self.stdin_executor(executeable_file)
        psutil_process = psutil.Process(process.pid)

        watcher_thread = threading.Thread(target=_watcher)
        watcher_thread.start()

        try:
            if input_type == 'STDIN':  # 标准输入
                stdout, stderr = self.stdin_communicate(
                    process, input_content, timeout=timeout)
            elif input_type == 'FILE':  # 文件输入
                stdout, stderr = self.file_communicate(
                    process, input_content, file_input_path, file_input_path.with_suffix('.out'), timeout=timeout)

            stdout: str = stdout.decode('utf-8')
            stderr: str = stderr.decode('utf-8')
        except subprocess.TimeoutExpired:
            return Status.TimeLimitExceeded, process_cpu_time.user + process_cpu_time.system, max_process_rss  # 返回 CPU 时间
        finally:
            signal = False  # 释放监测器

        if process.returncode != 0:
            return Status.RuntimeError, 0, max_process_rss

        # 返回 STDOUT, CPU 时间
        return stdout, process_cpu_time.user + process_cpu_time.system, max_process_rss

    def stdin_communicate(self, process: subprocess.Popen[bytes], input_content: str, timeout: float):
        return process.communicate(input_content.encode('utf-8'), timeout=timeout)

    def file_communicate(self, process: subprocess.Popen[bytes], input_content: str, file_input_path: pathlib.Path, output_file_path: pathlib.Path, timeout: float) -> Tuple[bytes, bytes]:
        process.wait(timeout=timeout)

        return output_file_path.read_bytes() if output_file_path.exists() else b'', b''

    def file_input_executor(self, executeable_file: pathlib.Path, file_input_path: pathlib.Path, input_content: str) -> subprocess.Popen[bytes]:
        executeable_file.parent.joinpath(file_input_path).write_text(
            input_content, encoding='utf-8')

        process = subprocess.Popen(
            executeable_file.absolute().__str__(),
            bufsize=-1,
            cwd=executeable_file.parent
        )

        return process

    def stdin_executor(self, executeable_file: pathlib.Path) -> subprocess.Popen[bytes]:
        process = subprocess.Popen(
            executeable_file.absolute().__str__(),
            bufsize=-1,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=executeable_file.parent
        )

        return process


# TODO: 暂缓开发安全运行时
# class SafetyRuntimeWithLrun(SimpleRuntime):
#     def __init__(self) -> None:
#         super().__init__()

#         if os.getuid() != 0 or os.getgid() != 0:  # pragma: no cover
#             raise RuntimeError('必须为 Root 用户才能使用 SafetyRuntimeWithLrun。')

#     def __call__(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN'] | Literal['FILE'], file_input_path: pathlib.Path = None, timeout: float = 1) -> str | Status:
#         if self.calling_precheck(executeable_file, input_content, input_type, file_input_path, timeout) is False:
#             return Status.RuntimeError

#         if input_type == 'STDIN':
#             self.stdin_executor(executeable_file, network=False, timeout=timeout, max_memory=0, uid=0, gid=0)

#     def stdin_executor(self, executeable_file: pathlib.Path, network: bool, timeout: float, max_memory: int, uid: int, gid: int) -> subprocess.Popen[bytes]:
#         # 注：max_memory 的单位为byte

#         process = subprocess.Popen(
#             [
#                 'sudo',
#                 'lrun',
#                 '--network', 'true' if network else 'false',
#                 '--max-cpu-time', str(timeout),
#                 '--max-memory', str(max_memory),
#                 '--isolate-process', 'true',
#                 '--uid', str(uid),
#                 '--gid', str(gid)
#             ]
#         )

#         return process


simple_runtime = SimpleRuntime()
