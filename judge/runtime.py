import os
import pathlib
import re
import shutil
import subprocess
import threading
from typing import Literal, Optional, Tuple, Union, overload

import psutil
import psutil._common
from rich.prompt import Prompt

import configs
from ccf_parser.status import Status
from utils import judge_logger


def match_result(text: list[str], pattern: str) -> str:
    return [x for x in text if pattern in x][0].replace(pattern, '').strip()


class SimpleRuntime(object):
    def __init__(self) -> None:
        pass

    def calling_precheck(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN', 'FILE'], file_input_path: Optional[pathlib.Path] = None, timeout: float = 1.0) -> bool:
        if file_input_path is not None:
            if file_input_path.is_absolute():
                judge_logger.warning(
                    f'执行评测时的输入文件路径 {file_input_path} 是绝对路径，正确的格式应当为 `Path("hello.in")` 一类。\n运行失败，返回状态码 RE。')
                return False

        executeable_file.chmod(0o700)

        return True

    def __call__(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN', 'FILE'], file_input_path: Optional[pathlib.Path] = None, timeout: float = 1.0, memory_limit: float = 128) -> Tuple[Union[str, Status], float, float]:
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
                if file_input_path is None:
                    raise ValueError('使用文件输入输出时，file_input_path 不可为 None')

                stdout, stderr = self.file_communicate(
                    process, input_content, executeable_file.parent.joinpath(file_input_path), executeable_file.parent.joinpath(file_input_path).with_suffix('.out'), timeout=timeout)

            stdout = stdout.decode('utf-8')
            stderr = stderr.decode('utf-8')
        except subprocess.TimeoutExpired:
            return Status.TimeLimitExceeded, process_cpu_time.user + process_cpu_time.system, max_process_rss  # 返回 CPU 时间
        finally:
            signal = False  # 释放监测器

        if process.returncode != 0:
            return Status.RuntimeError, process_cpu_time.user + process_cpu_time.system, max_process_rss

        if max_process_rss > memory_limit:
            return Status.MemoryLimitExceeded, process_cpu_time.user + process_cpu_time.system, max_process_rss

        # 返回 STDOUT, CPU 时间
        return stdout, process_cpu_time.user + process_cpu_time.system, max_process_rss

    def stdin_communicate(self, process: subprocess.Popen[bytes], input_content: str, timeout: float | None = None):
        return process.communicate(input_content.encode('utf-8'), timeout=timeout)

    def file_communicate(self, process: subprocess.Popen[bytes], input_content: str, file_input_path: pathlib.Path, output_file_path: pathlib.Path, timeout: float | None = None) -> Tuple[bytes, bytes]:
        """此处的 file_input_path 输入绝对路径"""
        process.wait(timeout=timeout)

        return output_file_path.read_bytes() if output_file_path.exists() else b'', process.stderr.read() if process.stderr is not None else b'NO STDERR'

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


class SafetyRuntime(SimpleRuntime):
    def __init__(self) -> None:
        super().__init__()

        # Root 用户检测
        if os.getuid() != 0 or os.getgid() != 0:  # pragma: no cover
            raise RuntimeError('必须为 Root 用户才能使用 SafetyRuntimeWithLrun。')

        # Lrun 存在检测
        output = subprocess.run('lrun', shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE).stderr.decode('utf-8')
        if not 'Run program with resources limited.' in output:  # pragma: no cover
            raise RuntimeError('Lrun 不存在')

    def __call__(self, executeable_file: pathlib.Path, input_content: str, input_type: Literal['STDIN'] | Literal['FILE'], file_input_path: pathlib.Path | None = None, timeout: float = 1, memory_limit: float = 128) -> Tuple[Union[str, Status], float, float]:
        """返回 STDOUT（STDOUT 无输出时返回第一个后缀为 .out 的文件的内容）或Status(运行失败)，运行所用的CPU时间(s)，运行所用的内存（MiB）"""
        if self.calling_precheck(executeable_file, input_content, input_type, file_input_path, memory_limit) is False:
            judge_logger.warning(f'{executeable_file} 的评测前预检不通过！')

            return Status.RuntimeError, 0, 0

        # 修改所有者
        os.chown(executeable_file, configs.LRUN_UID, configs.LRUN_GID)
        os.chmod(executeable_file, 0o777)

        # 启动进程
        if input_type == 'STDIN':
            process = self.stdin_executor(
                executeable_file=executeable_file, timeout=timeout, memory_limit=memory_limit)
        elif input_type == 'FILE':
            if file_input_path is None:
                raise ValueError('使用文件输入输出时，file_input_path 不可为 None')

            process = self.file_input_executor(executeable_file=executeable_file, file_input_path=file_input_path,
                                               input_content=input_content, timeout=timeout, memory_limit=memory_limit)

        # 交互
        if input_type == 'STDIN':
            output = self.stdin_communicate(process, input_content)
        elif input_type == 'FILE':  # 文件输入输出
            if file_input_path is None:
                raise ValueError('使用文件输入输出时，file_input_path 不可为 None')

            # 确保目录可读写
            os.chown(executeable_file.parent.joinpath(file_input_path.parent),
                     configs.LRUN_UID, configs.LRUN_GID)
            os.chown(executeable_file.parent.joinpath(file_input_path),
                     configs.LRUN_UID, configs.LRUN_GID)

            output = self.file_communicate(
                process, input_content, executeable_file.parent.joinpath(file_input_path), executeable_file.parent.joinpath(file_input_path).with_suffix('.out'))
        else:
            raise ValueError(
                '不支持的输入类型')  # pragma: no cover  # 由于是内部调用，而且有TypeHint，不可能发生，因此不覆盖该分支。

        # 分析
        stdout = output[0].decode('utf-8')
        stderr = output[1].decode('utf-8')

        stderr_splited = stderr.split('\n')

        memory = int(match_result(stderr_splited, 'MEMORY')) / \
            1048576  # 单位 MiB -> B
        cputime = float(match_result(stderr_splited, 'CPUTIME'))
        realtime = float(match_result(stderr_splited, 'REALTIME'))
        exitcode = int(match_result(stderr_splited, 'EXITCODE'))
        exceed: Literal['none', 'CPU_TIME', 'REAL_TIME',
                        'MEMORY', 'OUTPUT'] | str = match_result(stderr_splited, 'EXCEED')

        if exitcode != 0:
            return Status.RuntimeError, cputime, memory  # 返回值非0，返回 CPU 时间，内存占用

        if exceed == 'CPU_TIME':
            return Status.TimeLimitExceeded, cputime, memory  # 超时，返回 CPU 时间，内存占用
        elif exceed == 'REAL_TIME':
            return Status.TimeLimitExceeded, cputime, memory  # 超时，返回 CPU 时间，内存占用
        elif exceed == 'MEMORY':
            return Status.MemoryLimitExceeded, cputime, memory  # 超内存，返回 CPU 时间，内存占用

        return stdout, cputime, memory  # 返回 STDOUT, CPU 时间，内存占用

    def stdin_executor(self, executeable_file: pathlib.Path, timeout: float = 1, memory_limit: float = 128) -> subprocess.Popen[bytes]:
        return subprocess.Popen(
            ' '.join([
                'lrun',
                '--uid', str(configs.LRUN_UID),
                '--gid', str(configs.LRUN_GID),
                '--network', 'false',
                '--max-cpu-time', str(timeout),
                '--max-real-time', str(timeout * 2),
                # 单位 MiB -> B
                '--max-memory', str({memory_limit * 1024 * 1024}),
                '--isolate-process', 'false',
                '--max-nprocess', '1',
                '--reset-env', 'true',
                executeable_file.absolute().__str__(),
                '3>&2'
            ]),
            cwd=executeable_file.parent,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=-1,
            shell=True
        )

    def file_input_executor(self, executeable_file: pathlib.Path, file_input_path: pathlib.Path, input_content: str, timeout: float = 1, memory_limit: float = 128) -> subprocess.Popen[bytes]:
        # 写入输入文件
        executeable_file.parent.joinpath(file_input_path).write_text(
            input_content, encoding='utf-8')

        return self.stdin_executor(executeable_file=executeable_file, timeout=timeout, memory_limit=memory_limit)


def choose_runtime() -> Union[SimpleRuntime, SafetyRuntime]:  # pragma: no cover
    if os.getuid() == 0 and os.getgid() == 0:  # Root 用户检测
        return SafetyRuntime()  # 返回 SafetyRuntime 实例
    else:  # 非 Root 用户检测，返回 SimpleRuntime 实例
        judge_logger.warning('没有以 Root 用户运行，使用简单运行时(不安全)')
        return SimpleRuntime()


runtime = choose_runtime()
