
import mysql.connector


class Model:
    def __init__(self):
        dbname = 'demo_practice'
        user = 'root'
        password = '0000'
        host = 'localhost'
        # port = '3306'
        try:
            self.conn = mysql.connector.connect(database=dbname, user=user, password=password, host=host)
            
        except mysql.connector.Error as er:
            print(er)