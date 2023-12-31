from enum import Enum


class ExecOutcome(Enum):
    PASSED = "PASSED"
    WRONG_ANSWER = ("WRONG_ANSWER")
    TIME_LIMIT_EXCEEDED = "TIME_LIMIT_EXCEEDED"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    COMPILATION_ERROR = "COMPILATION_ERROR"
    MEMORY_LIMIT_EXCEEDED = ("MEMORY_LIMIT_EXCEEDED")
