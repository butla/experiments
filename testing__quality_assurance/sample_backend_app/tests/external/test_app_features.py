"""
This is a sample external tests' file.
"""

import uuid

import httpx

APP_ADDRESS = "http://localhost:8080"


def test_store_and_retrieve_notes():
    # TODO add a note, read it by the ID
    # add one more note
    # See that they're both in the result when you get all notes
    # result should not match the whole returned thing, since there might be more data there.
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
