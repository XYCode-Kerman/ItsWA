import shutil
from pathlib import Path

from ccf_parser import CCF, CheckPointResult, JudgingResult
from ccf_parser.status import Status
from utils import judge_logger

from .languages import CPP
from .runtime import runtime


class Player(object):
    def __init__(self, name: str, order: str, path: Path) -> None:
        self.name = name
        self.order = order
        self.path = path

    def judging(self, ccf: CCF) -> JudgingResult:
        judging_result = JudgingResult(
            player_order=self.order, problems_result={})

        # 逐题评测
        for problem in ccf.contest.problems:
            judging_result.problems_result[problem.name] = []

            # 题目文件夹
            problem_dir = Path.joinpath(
                ccf.header.path,
                'players',
                self.order,
                problem.judge_config.source_file_name,
            )

            # 语言合法性检测
            if problem_dir.joinpath(f'{problem.judge_config.source_file_name}.cpp').exists() and 'CPP' in problem.judge_config.languages:
                # 使用C++编译器进行编译
                compiled = problem_dir.joinpath('compiled', 'sol')
                compiled.parent.mkdir(exist_ok=True)

                compile_result = CPP().compile(
                    problem_dir.joinpath(
                        f'{problem.judge_config.source_file_name}.cpp'),
                    compiled
                )

                if compile_result is False:
                    judge_logger.warning(
                        f'{problem_dir.joinpath(f"{problem.judge_config.source_file_name}.cpp").absolute()} 编译失败。')

                    for ckpt in problem.judge_config.checkpoints:
                        judging_result.problems_result[problem.name].append(
                            CheckPointResult(
                                ckpt=ckpt,
                                score=0,
                                status=Status.CompileError,
                                output=''
                            )
                        )
                else:
                    # 测试点结果
                    for ckpt in problem.judge_config.checkpoints:
                        running_result, running_time, running_memory = runtime(
                            compiled,
                            ckpt.input,
                            ckpt.input_type,
                            ckpt.input_file
                        )

                        if isinstance(running_result, str):
                            # AC
                            if ckpt.compare(running_result):
                                judging_result.problems_result[problem.name].append(
                                    CheckPointResult(
                                        ckpt=ckpt,
                                        score=ckpt.ckpt_score,
                                        status=Status.Accepted,
                                        output=running_result,
                                        time=running_time,
                                        memory=running_memory
                                    )
                                )
                            else:
                                judging_result.problems_result[problem.name].append(
                                    CheckPointResult(
                                        ckpt=ckpt,
                                        score=0,
                                        status=Status.WrongAnswer,
                                        output=running_result,
                                        time=running_time,
                                        memory=running_memory
                                    )
                                )
                        else:
                            judging_result.problems_result[problem.name].append(
                                CheckPointResult(
                                    ckpt=ckpt,
                                    score=0,
                                    status=running_result,
                                    output='',
                                    time=running_time,
                                    memory=running_memory
                                )
                            )

                    # 清理编译结果
                    shutil.rmtree(compiled.parent, ignore_errors=True)
            else:
                judge_logger.warning(
                    f'{problem_dir.joinpath(f"{problem.judge_config.source_file_name}.cpp").absolute()} 不存在或是不符合题目配置的编程语言。')
                for ckpt in problem.judge_config.checkpoints:
                    judging_result.problems_result[problem.name].append(
                        CheckPointResult(
                            ckpt=ckpt,
                            score=0,
                            status=Status.CompileError,
                            output=''
                        )
                    )

        return judging_result
