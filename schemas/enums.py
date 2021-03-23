import enum


class ResultEnum(enum.Enum):
    Accepted = 1
    WrongAnswer = 2
    TimeLimitExceeded = 3
    MemoryLimitExceeded = 4
    RuntimeError = 5
    OutputLimitExceeded = 6
    CompileError = 7
    PresentationError = 8
    SystemError = 9
    # ...
    Unknown = 999


class LanguageEnum(enum.Enum):
    C = 1
    Cpp = 2
    Python = 3
    Java = 4
    Go = 5
    Rust = 6
    JavaScript = 7
    TypeScript = 8
    Unknown = 999

