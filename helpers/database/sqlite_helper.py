import sqlite3

class SQLiteHelper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            print("Connected to SQLite database")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            # print("Query executed successfully")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    def fetch_data(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Error fetching data: {e}")
        finally:
            cursor.close()

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("SQLite connection closed")
