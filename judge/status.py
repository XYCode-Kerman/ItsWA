from enum import Enum


class Status(Enum):
    Accepted = 'AC'
    CompileError = 'CE'
    WrongAnswer = 'WA'
    RuntimeError = 'RE'
    TimeLimitExceeded = 'TLE'
    MemoryLimitExceeded = 'MLE'
    OutputLimitExceeded = 'OLE'
