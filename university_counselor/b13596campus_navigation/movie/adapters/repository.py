import abc
from typing import List
from datetime import date



repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def load_movies(self) -> List[None]:
        """ Returns the Tags stored in the repository. """
        raise NotImplementedError