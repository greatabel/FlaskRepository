from datetime import date, datetime
from typing import List

import pytest

from movie.domain.model import Movie
from movie.adapters.repository import RepositoryException


# def test_repository_load_movies(in_memory_repo):

#     assert len(in_memory_repo.load_movies() ) > 0