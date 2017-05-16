import io
import json
import select
import signal
import subprocess
import sys
import time

import mountepy
import mountepy.mountebank
import pytest

import tests.common


@pytest.fixture
def url_to_find():
    yield 'http://example.com/just-some_url'


@pytest.fixture
def fake_site_url(url_to_find: str):
    html = tests.common.HTML_WITH_EMPTY_BODY.format(
        f"""<p>This is just some text</p>
        <a href="{url_to_find}">Here's a link</a>""")
    with mountepy.Mountebank() as mb:
        site_impostor = mb.add_imposter_simple(response=html)
        yield f'http://localhost:{site_impostor.port}'


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
        if line_selector.poll(0.01):
            return stream.readline()
    pytest.fail('Waiting for a stream line timed out.')


def _close_app_process(process: subprocess.Popen):
    # SIGINT instead of terminate,
    # so that subprocess coverage works without special signal handling
    process.send_signal(signal.SIGINT)
    try:
        process.wait(3)
    except subprocess.TimeoutExpired:
        process.kill()
        pytest.fail("The process didn't close on time.")


def test_scraping_urls_with_a_producer_and_consumer(
        fake_site_url: str,
        url_to_find: str,
        redis_port: int):
    url_extractor_process = subprocess.Popen(
        [sys.executable, '-m', 'txodds_code_test.url_extractor', 'localhost', str(redis_port)],
        stdout=subprocess.PIPE)
    try:
        html_extractor_process = subprocess.Popen(
            [sys.executable, '-m', 'txodds_code_test.html_extractor',
             'localhost', str(redis_port), fake_site_url])
        html_extractor_process.wait(3)

        json_output_line = _wait_for_line_in_stream(url_extractor_process.stdout, 3)
        assert {fake_site_url: [url_to_find]} == json.loads(json_output_line)
    finally:
        _close_app_process(url_extractor_process)
