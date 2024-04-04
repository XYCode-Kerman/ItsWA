from pathlib import Path

from ccf_parser import CCF


def init_contest(ccf: CCF, path: Path):  # pragma: no cover
    if not path.exists():
        raise FileNotFoundError("比赛目录不存在")

    if path.is_dir():
        raise IsADirectoryError("比赛目录是一个文件夹")

    players_dir = path.joinpath('players')
    ccf_path = path.joinpath('ccf.json')

    players_dir.mkdir(exist_ok=True)
    ccf_path.touch(exist_ok=True)

    ccf_path.write_text(ccf.model_dump_json(indent=4))
