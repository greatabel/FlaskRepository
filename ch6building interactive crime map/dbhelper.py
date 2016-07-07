import pymysql
import dbconfig


class DBHelper:

    def connect(self, database="crimemap"):
        return pymysql.connect(host='localhost',
                               user=dbconfig.db_user,
                               passwd=dbconfig.db_password,
                               db=database)

    def get_all_inputs(self):
        connection = self.connect()
        try:
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def get_rawmeasure(self, userid):
        connection = self.connect()
        try:
            query = "SELECT * FROM MeasureRaw;"
            if userid is not None:
                query = "SELECT MeasureRaw.* FROM MeasureRaw,Patient_User " \
                        "where MeasureRaw.patientid = Patient_User.patientid and Patient_User.userid=" + userid + ";"
            with connection.cursor() as cursor:
                cursor.execute(query)
            return cursor.fetchall()
        finally:
            connection.close()

    def add_rawmeasure(self, args):
        connection = self.connect()
        try:
            query = "insert MeasureRaw( rawdata, patientid, whicheye, createdate) values(%s, %s, %s, now());"
            with connection.cursor() as cursor:
                cursor.execute(query, ( args['rawdata'], 0,args['whicheye']))
                connection.commit()
        finally:
            connection.close()

    # def get_measure(self):
    #     connection = self.connect()
    #     try:
    #         query = "SELECT * FROM Measure;"
    #         with connection.cursor() as cursor:
    #             cursor.execute(query)
    #         return cursor.fetchall()
    #     finally:
    #         connection.close()

    # def add_measure(self, args):
    #     connection = self.connect()
    #     try:
    #         query = "insert Measure(rawdataid, data, deviceid,createdate) values(%s, %s, %s, now());"
    #         with connection.cursor() as cursor:
    #             cursor.execute(query, (4, args['data'], args['deviceid']))
    #             connection.commit()
    #     finally:
    #         connection.close()

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            print('query=', query)
            with connection.cursor() as cursor:
                cursor.execute(query, data)
                connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
        finally:
            connection.close()
