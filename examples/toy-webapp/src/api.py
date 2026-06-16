"""Toy API — the source the claim graph resolves against. Intentionally boring."""

def handle_request(req):
    """Top-level HTTP handler: parse, persist, enqueue."""
    data = _parse(req)
    save_user(data)
    enqueue_job(data)
    return 200

def save_user(data):
    """Persist a user record to sqlite."""
    DB.execute("INSERT INTO users VALUES (?)", data)

def enqueue_job(data):
    """Publish a background job to the queue."""
    QUEUE.put(data)
