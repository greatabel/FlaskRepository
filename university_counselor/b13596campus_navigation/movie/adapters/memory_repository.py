import csv
import os
from datetime import date, datetime
from typing import List






class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        


