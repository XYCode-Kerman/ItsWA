import json
import pathlib

from ccf_parser import CCF
from judge import start_judging

ccf = CCF(
    **json.loads(pathlib.Path('./temp/test_contest/ccf.json').read_text(encoding='utf-8'))
)

start_judging(ccf)
