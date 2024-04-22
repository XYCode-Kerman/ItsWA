import abc
import pathlib
import shlex
import subprocess
from typing import List

from utils import judge_logger

from .filter import CPPFilter


class Language(abc.ABC):
    def __init__(self) -> None:
        self.name: str = 'Language Name'
        self.compiler: str = 'Compiler Command'
        self.compile_options: List[str] = ['Option 1', 'Option 2']
        self.suffix = ''

    @abc.abstractmethod
    def compile(self, source: pathlib.Path, output: pathlib.Path) -> bool:
        pass  # pragma: no cover


class CPP(Language):
    def __init__(self) -> None:
        super().__init__()
        self.name = 'CPP'
        self.suffix = 'cpp'
        self.compiler = 'g++'
        self.compile_options = ['-O2', '-std=c++14']
        self.filter = CPPFilter()

    def pre_compile_check(self, source: pathlib.Path, output: pathlib.Path) -> bool:
        # 编译前检查
        if not source.exists():
            judge_logger.debug(f'源代码文件 {source} 不存在')
            return False

        code = source.read_text(encoding='utf-8')

        if self.filter.filter(code) is False:
            judge_logger.debug(f'源代码文件 {source} 包含非法代码！')

            return False

        return True

    def compile(self, source: pathlib.Path, output: pathlib.Path) -> bool:
        if not self.pre_compile_check(source, output):
            judge_logger.warning(f'{source} 的编译前检查失败。')
            return False

        cmd = [
            self.compiler,
            *self.compile_options,
            str(source.absolute()),
            '-o', str(output.absolute()),
        ]

        process = subprocess.Popen(
            shlex.join(cmd),
            shell=True
        )

        process.wait()

        if process.returncode != 0:
            judge_logger.warning(f'编译 {source} 失败，返回值为 {process.returncode}')
            return False
        elif not output.exists():
            judge_logger.warning(
                f'编译 {source} 成功，但目标文件 {output} 不存在')  # pragma: no cover
            return False  # pragma: no cover
        else:
            return True
