from datetime import date

from movie.domain.model import Movie, User, Review

import pytest


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')

def test_user(user):
    assert user.user_name == 'dbowie'


@pytest.fixture()
def movie():
    return Movie('matrix', 1998, 1)


def test_movie(movie):
    assert movie.title == 'matrix'
    assert movie.release_year == 1998
    assert movie.id == 1


@pytest.fixture()
def review():
    m = Movie('matrix', 1998, 1)
    return Review(m, 'good movie!', 5)

def test_review(review):
    assert review.movie.id == 1
    assert review.review_text == 'good movie!'
    assert review.rating == 5