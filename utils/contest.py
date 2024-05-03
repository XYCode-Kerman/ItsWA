import pathlib

from ccf_parser import CCF


def init_contest(path: pathlib.Path, ccf: CCF):
    path.mkdir(exist_ok=True, parents=True)
    path.joinpath('players').mkdir(exist_ok=True)
    path.joinpath('ccf.json').write_text(
        ccf.model_dump_json(indent=4), encoding='utf-8')
