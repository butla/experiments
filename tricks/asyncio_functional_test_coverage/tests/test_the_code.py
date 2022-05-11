from pathlib import Path
import subprocess
import sys

import pytest

from the_code import main


# @pytest.mark.asyncio
# async def test_the_code_unit():
#     await main.main()


def test_the_code_functional():
    script_path = (Path(__file__) / '../../the_code/main.py').resolve()
    proc = subprocess.Popen([sys.executable, str(script_path)])
    assert proc.wait(10) == 0
