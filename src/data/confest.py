import json
import os

import pytest

TEST_FILES = [
    "src/data/test_bookings.json",
    "src/data/test_rooms.json",
    "src/data/test_users.json",
]


@pytest.fixture(autouse=True)
def clean_test_files():
    for path in TEST_FILES:
        if os.path.exists(path):
            with open(path, "w") as f:
                json.dump([], f)
