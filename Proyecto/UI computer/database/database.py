import sqlite3


class DB:
    connection = sqlite3.connect("./database/app.db", check_same_thread=False)
    cursor = connection.cursor()

    def searchStudent(self, num_control, password):
        result = self.cursor.execute(
            f"SELECT * FROM 'main'.'User' WHERE num_control='{num_control}' AND password='{password}'")
        request = result.fetchall()
        if len(request) == 1:
            return request[0]
        else:
            return False

    def getAllStudents(self):
        result = self.cursor.execute(f"SELECT * FROM User")
        return result.fetchall()

    def getStudent(self, num_control):
        result = self.cursor.execute(
            f"SELECT * FROM 'main'.'User' WHERE num_control='{num_control}'")
        request = result.fetchall()
        if len(request) > 0:
            return request[0]
        else:
            return False

    def storeStudent(self, num_control, username, password):
        self.cursor.execute(f"INSERT INTO 'main'.'User' (num_control, username, password) VALUES ('{num_control}', '{username}', '{password}')")
        self.connection.commit()

    def updateStudent(self, num_control, username, password):
        self.cursor.execute(f"UPDATE 'main'.'User' SET username = '{username}', password = '{password}' WHERE num_control = '{num_control}'")
        self.connection.commit()

    def deleteStudent(self, num_control):
        self.cursor.execute(f"DELETE FROM 'main'.'User' WHERE num_control = '{num_control}'")
        self.connection.commit()
