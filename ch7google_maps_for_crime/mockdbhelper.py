class MockDBHelper:

    def connect(self, database="crimemap"):
        pass

    def add_crime(self, category, date, latitude, longitude, description):
        data = [category, date, latitude, longitude, description]
        for i in data:
            print(i, type(i))