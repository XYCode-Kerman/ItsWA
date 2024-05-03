from manager import cli_app, start_server_background
from ccf_parser import CCF
import json
import pathlib

import dotenv

dotenv.load_dotenv()


if '__main__' == __name__:
    cli_app()
    # start_server_background()
