import datetime
from typing import List

import dominate  # type: ignore
from dominate.tags import (div, h1, link, p, script, table,  # type: ignore
                           tbody, td, th, thead, tr)

from ccf_parser import JudgingResult


class ReportAnalyze(object):
    def __init__(self, judging_results: List[JudgingResult]) -> None:
        self.judging_results = judging_results

    def generate(self) -> str:
        """生成HTML报告

        Returns:
            str: HTML文档
        """

        doc = dominate.document(
            title=f'评测结果分析 | 生成于 {datetime.datetime.now()}')

        with doc.head:
            script(src='https://cdn.tailwindcss.com')
            link(href="https://cdn.jsdelivr.net/npm/daisyui@4.9.0/dist/full.min.css",
                 rel="stylesheet", type="text/css")

        with doc.body:
            with div(cls='text-center w-screen p-16 flex justify-center items-center flex-col'):
                h1('评测结果分析', cls='text-xl font-bold')

                with table(cls='table'):
                    # 表头
                    with thead():
                        with tr():
                            th()  # 表格序号（不是选手序号）
                            th('选手序号')

                            # 题目
                            for problem_name in self.judging_results[0].problems_result.keys():
                                th(problem_name)

                            th('总分')

                    # 表
                    with tbody():
                        for player_index, player in enumerate(self.judging_results):
                            with tr():
                                th(player_index)
                                td(player.player_order)

                                # 题目
                                for problem in player.problems_result.values():
                                    with td().add(
                                        div(
                                            cls='tooltip',
                                            data_tip='\n'.join([
                                                f'测试点 {
                                                    idx + 1}: {x.status.value}'
                                                for idx, x in enumerate(problem)
                                            ])
                                        )
                                    ):
                                        p(sum({
                                            ckpt.score
                                            for ckpt in problem
                                        }))

                                # 总分
                                td(sum({
                                    sum({
                                        ckpt.score
                                        for ckpt in x
                                    })
                                    for x in player.problems_result.values()
                                }))

        return doc.render()
