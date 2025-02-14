from pprint import pformat
from subprocess import run
from pylint.lint import Run
import pytest

@pytest.fixture(scope="class")
def pylint_results(source_files):
    print(f"Checking files:\n{pformat(source_files)}")
    return Run(["--disable=dangerous-default-value,too-many-arguments,too-few-public-methods"] + source_files, exit=False).linter.stats.global_note

class TestStyle:

    def test_20pc(self, pylint_results):
        assert pylint_results >= 2.

    def test_40pc(self, pylint_results):
        assert pylint_results >= 4.

    def test_60pc(self, pylint_results):
        assert pylint_results >= 6.

    def test_80pc(self, pylint_results):
        assert pylint_results >= 8.

    def test_90pc(self, pylint_results):
        assert pylint_results >= 9.


class TestDocumentation:

    def test_documentation_present(self, source_files_str):
        cmd = rf'pydocstyle --select=D100,D102,D103,D419 {source_files_str}'
        res = run(cmd, shell=True, capture_output=True, check=False, text=True)
        if res.returncode:
            print("pydocstyle")
            print("---------")
            print(f"cmd:\n{cmd}")
            print(f"return code: {res.returncode}")
            print(f"stderr:\n{res.stderr}")
            assert not res.stderr, "Problem running pydocstyle command."
        missing_docs = len(res.stdout.splitlines()) / 2
        if missing_docs:
            print(f"Num of problems: {missing_docs}")
            print(f"stdout:\n{res.stdout}")
        assert missing_docs == 0

    def test_documentation_style(self, source_files_str):
        cmd = rf'darglint {source_files_str}'
        res = run(cmd, shell=True, capture_output=True, check=False, text=True)
        if res.returncode:
            print("darglight")
            print("---------")
            print(f"cmd:\n{cmd}")
            print(f"return code: {res.returncode}")
            print(f"stderr:\n{res.stderr}")
            assert not res.stderr, "Problem running darglint command."
        malformed_docs = max(len(res.stdout.splitlines()) - 1, 0)
        if malformed_docs:
            print(f"Num of problems: {malformed_docs}")
            print(f"stdout:\n{res.stdout}")
        assert malformed_docs == 0
