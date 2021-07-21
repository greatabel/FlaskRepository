import os
import pytest

from movie import create_app
from movie.adapters import memory_repository
from movie.adapters.memory_repository import MemoryRepository


TEST_DATA_PATH = os.path.join("movie", "tests", "data")
# TEST_DATA_PATH = os.path.join('C:', os.sep, 'Users', 'iwar006', 'Documents', 'Python dev', 'COVID-19', 'tests', 'data')


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()

    return repo


@pytest.fixture
def client():
    my_app = create_app(
        {
            "TESTING": True,  # Set to True during testing.
            "TEST_DATA_PATH": TEST_DATA_PATH,  # Path for loading test data into the repository.
            "WTF_CSRF_ENABLED": False,  # test_client will not send a CSRF token, so disable validation.
        }
    )

    return my_app.test_client()
