from pathlib import Path
from shutil import copyfile
from subprocess import run

from coblack import format_file


test_data_dir = Path(__file__).parent / "data"
# fmt:off
_input_file          = test_data_dir / "input.py"
temp_file            = test_data_dir / "temp.py"
expected_output_file = test_data_dir / "expected_output.py"
# fmt:on


def reset_temp_file():
    copyfile(_input_file, temp_file)


def test_format_file():
    reset_temp_file()
    format_file(temp_file)
    assert temp_file.read_text() == expected_output_file.read_text()


def test_cli():
    reset_temp_file()
    result = run(["coblack", str(temp_file)])
    assert result.returncode == 0
    assert temp_file.read_text() == expected_output_file.read_text()


def test_cli_not_a_file():
    result = run(["coblack", "C:/"])
    assert result.returncode != 0
