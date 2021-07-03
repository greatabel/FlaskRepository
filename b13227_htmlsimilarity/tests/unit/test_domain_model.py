from datetime import date

from movie.domain.model import Movie, User, Review

import pytest


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')

def test_user(user):
    assert user.user_name == 'dbowie'


