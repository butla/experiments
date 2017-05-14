import io
import json
from pathlib import Path
import select
import subprocess
import sys
import time
from typing import List

import mountepy
import mountepy.mountebank
import pytest


@pytest.fixture
def url_to_find():
    yield 'http://example.com/just-some_url'


@pytest.fixture
def fake_site_url(url_to_find: str):
    html = f"""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
  <head>
    <title>Just some page</title>
  </head>
  <body>
    <p>This is just some text</p>
    <a href="{url_to_find}">Here's a link</a>
  </body>
</html>"""
    with mountepy.Mountebank() as mb:
        site_impostor = mb.add_imposter_simple(response=html)
        yield f'http://localhost:{site_impostor.port}'


APP_CODE_DIR = (Path(__file__) / '../../../txodds_code_test').resolve()  # pylint: disable=no-member


def _start_app_process(
        process_file: Path,
        redis_port: int,
        args: List[str] = None) -> subprocess.Popen:
    if not args:
        args = []
    return subprocess.Popen(
        [sys.executable, str(process_file), 'localhost', str(redis_port)] + args,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE)


def _close_app_process(process: subprocess.Popen):
    process.terminate()
    try:
        process.wait(3)
    except subprocess.TimeoutExpired:
        process.kill()
        pytest.fail("The process didn't close on time.")


def _wait_for_line_in_stream(stream: io.BufferedReader, timeout: float) -> str:
    """Wait for a line to appear in a stream and return it.

    This will only work on Unix.
    If something does appear in the stream, but it isn't terminated with a newline, then this
    function will hang. But since the program that we will use this for will write its output in
    lines, I don't think that the additional robustness is needed.
    """
    line_selector = select.poll()
    line_selector.register(stream, select.POLLIN)
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < timeout:
        if line_selector.poll():
            return stream.readline()


def test_scraping_urls_with_a_producer_and_consumer(
        fake_site_url: str,
        url_to_find: str,
        redis_port: int):
    html_extractor_script = APP_CODE_DIR / 'html_extractor.py'
    html_extractor_process = _start_app_process(
        html_extractor_script, redis_port, [fake_site_url + '\n'])
    _close_app_process(html_extractor_process)

    url_extractor_script = APP_CODE_DIR / 'url_extractor.py'
    url_extractor_process = _start_app_process(url_extractor_script, redis_port)
    try:
        json_output_line = _wait_for_line_in_stream(url_extractor_process.stdout, 3)
        assert {fake_site_url: [url_to_find]} == json.loads(json_output_line)
    finally:
        _close_app_process(url_extractor_process)
