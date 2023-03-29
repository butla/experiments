"""
This is a sample external tests' file.
"""

import uuid

import httpx
import pytest
import tenacity

APP_ADDRESS = "http://localhost:8080"


# Scope is session, so that this fixture runs only once during the test suite.
# If we'd have more tests, we don't need to go through waiting for the app again.
@pytest.fixture(scope="session")
def app_url():
    _wait_for_http_url(APP_ADDRESS)
    return APP_ADDRESS


@tenacity.retry(stop=tenacity.stop_after_delay(10), wait=tenacity.wait_fixed(0.2), reraise=True)
def _wait_for_http_url(url: str):
    result = httpx.get(url)
    if result.status_code != 200:
        raise ValueError("App returned the wrong status code")


def test_store_and_retrieve_note(app_url):
    note_contents = f"first note {uuid.uuid4()}"
    create_result = httpx.post(
        f"{APP_ADDRESS}/notes/",
        json={"contents": note_contents},
    )
    assert create_result.status_code == 201
    assert create_result.json()["contents"] == note_contents
    note_id = create_result.json()["id"]

    get_result = httpx.get(f"{APP_ADDRESS}/notes/{note_id}/")
    assert get_result.status_code == 200
    assert get_result.json()["contents"] == note_contents

    get_all_result = httpx.get(f"{APP_ADDRESS}/notes/")
    assert next(note for note in get_all_result.json() if note["id"] == note_id)
