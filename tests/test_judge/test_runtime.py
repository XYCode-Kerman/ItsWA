import json
import os
import pathlib
import tempfile
import uuid
from pathlib import Path

import pytest

from ccf_parser import CCF, CheckPoint, JudgingResult
from ccf_parser.status import Status
from judge import ReportAnalyze, simple_judging, start_judging
from judge.languages import CPP, Language
from judge.runtime import SafetyRuntime, SimpleRuntime, runtime

simple_runtime = SimpleRuntime()
# Root
if os.getuid() == 0 and os.getgid() == 0:
    safety_runtime = SafetyRuntime()
else:
    safety_runtime = SimpleRuntime()


def test_simple_runtime():
    for input_type in ['STDIN', 'FILE']:
        assert simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/tle'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0] == Status.TimeLimitExceeded

        assert simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/re'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0] == Status.RuntimeError

        assert type(simple_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/ac'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0]) in [Status, str]

    assert simple_runtime(
        pathlib.Path('./tests/environment/executeables_to_test/ac'),
        '',
        input_type,
        pathlib.Path('/tmp/a.in')
    )[0] == Status.RuntimeError


def test_safety_runtime():
    for input_type in ['STDIN', 'FILE']:
        assert safety_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/tle'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0] == Status.TimeLimitExceeded

        assert safety_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/re'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0] == Status.RuntimeError

        assert type(safety_runtime(
            pathlib.Path('./tests/environment/executeables_to_test/ac'),
            '',
            input_type,
            pathlib.Path('a.in')
        )[0]) in [Status, str]

    assert safety_runtime(
        pathlib.Path('./tests/environment/executeables_to_test/ac'),
        '',
        input_type,
        pathlib.Path('/tmp/a.in')
    )[0] == Status.RuntimeError
