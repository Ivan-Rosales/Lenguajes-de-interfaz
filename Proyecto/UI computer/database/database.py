import sqlite3


class DB:
    connection = sqlite3.connect("./database/app.db", check_same_thread=False)
    cursor = connection.cursor()

    def searchStudent(self, num_control, password):
        result = self.connection.execute(
            f"SELECT * FROM User WHERE num_control='{num_control}' AND password='{password}'"
        )
        request = result.fetchall()
        if len(request) == 1:
            return request[0]
        else:
            return False