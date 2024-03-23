from pathlib import Path
from typing import Dict, List, Union

from ccf_parser import CCF
from utils import judge_logger

from .languages import CPP
from .runtime import simple_runtime
from .status import Status


class Player(object):
    def __init__(self, name: str, order: str, path: Path) -> None:
        self.name = name
        self.order = order
        self.path = path

    def judging(self, ccf: CCF) -> Dict[str, List[Status]]:
        results: Dict[str, List[Status]] = {}
        for key in ccf.contest.problems:
            results[key.name] = []

        for problem in ccf.contest.problems:
            problem_dir = Path.joinpath(
                ccf.header.path,
                'players',
                self.order,
                problem.judge_config.source_file_name,
            )

            if problem_dir.joinpath(f'{problem.judge_config.source_file_name}.cpp').exists() and 'CPP' in problem.judge_config.languages:
                # 使用C++编译器进行编译
                compiled = problem_dir.joinpath('compiled', 'sol')
                compiled.parent.mkdir(exist_ok=True)

                result = CPP().compile(
                    problem_dir.joinpath(
                        f'{problem.judge_config.source_file_name}.cpp'),
                    compiled
                )

                if result is False:
                    judge_logger.warning(
                        f'{problem_dir.joinpath(f"{problem.judge_config.source_file_name}.cpp").absolute()} 编译失败。')
                    results[problem.name].append(Status.CompileError)
                else:
                    # 开始评测
                    for ckpt in problem.judge_config.checkpoints:
                        result: Union[str, Status] = simple_runtime(
                            compiled,
                            ckpt.input,
                            ckpt.input_type,
                            ckpt.input_file
                        )

                        if isinstance(result, str):
                            # 比较
                            if ckpt.compare(result):
                                results[problem.name].append(Status.Accepted)
                            else:
                                results[problem.name].append(
                                    Status.WrongAnswer)
                        elif isinstance(result, Status):
                            results[problem.name].append(result)
            else:
                judge_logger.warning(
                    f'{problem_dir.joinpath(f"{problem.judge_config.source_file_name}.cpp").absolute()} 不存在或是不符合题目配置的编程语言。')
                results[problem.name].append(Status.CompileError)

        return results
