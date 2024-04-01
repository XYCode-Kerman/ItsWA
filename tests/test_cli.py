from pathlib import Path

import pytest
from typer.testing import CliRunner

from manager import cli_app


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_intro(cli_runner: CliRunner):
    result = cli_runner.invoke(cli_app, ["intro"])

    assert result.exit_code == 0
    assert "欢迎使用 ItsWA 评测系统" in result.stdout


def test_start_judging(cli_runner: CliRunner, temp_contest: Path):
    result = cli_runner.invoke(
        cli_app, ["judge", "start", temp_contest.joinpath('ccf.json').absolute().__str__()])
    assert result.exit_code == 0

    result = cli_runner.invoke(
        cli_app, ["judge", "start", temp_contest.joinpath('114514').absolute().__str__()])
    assert result.exit_code != 0

    result = cli_runner.invoke(
        cli_app, ["judge", "start", temp_contest.absolute().__str__()])
    assert result.exit_code == 0

    # 分析
    result = cli_runner.invoke(
        cli_app, ["judge", "analyze", temp_contest.joinpath('judging_results.json').absolute().__str__()])
    assert result.exit_code == 0
    assert temp_contest.joinpath('report.html').exists() is True

    assert cli_runner.invoke(
        cli_app, ["judge", "analyze", temp_contest.joinpath('foo').absolute().__str__()]).exit_code != 0
    assert cli_runner.invoke(
        cli_app, ["judge", "analyze", temp_contest.joinpath('players').absolute().__str__()]).exit_code != 0
