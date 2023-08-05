from pathlib import Path
import pytest
from tuxmake.log import LogParser

logs = Path(__file__).parent / "logs"


class TestLogParser:
    @pytest.mark.parametrize(
        "log,errors,warnings",
        (
            ("compiler-lacks.log", 1, 0),
            ("invalid-config.log", 1, 0),
            ("compiler-not-found.log", 1, 0),
            ("simple.log", 1, 1),
            ("case.log", 3, 3),
            ("no-such-file-or-directory.log", 1, 5),
        ),
    )
    def test_log(self, log, errors, warnings):
        parser = LogParser()
        parser.parse(logs / log)
        assert (parser.errors, parser.warnings) == (errors, warnings)
