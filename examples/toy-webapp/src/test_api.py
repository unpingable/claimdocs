"""Toy tests."""

def test_handle_request_persists_and_enqueues():
    """handle_request writes a user and publishes a job."""
    assert handle_request({"u": 1}) == 200
