from helpers.database.sqlite_helper import SQLiteHelper
from datetime import datetime

class Log:
    def __init__(self, db_name="assets/databases/log.db"):
        self.db_helper = SQLiteHelper(db_name)
        self.db_helper.connect()
        self.create_log_table()

    def create_log_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            status TEXT NOT NULL
        );
        """
        self.db_helper.execute_query(create_table_query)

    def add_log(self, status):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_query = "INSERT INTO logs (date, status) VALUES (?, ?)"
        self.db_helper.execute_query(insert_query, (date, status))

    def get_logs(self):
        select_query = "SELECT * FROM logs"
        return self.db_helper.fetch_data(select_query)

    def update_log(self, log_id, status):
        update_query = "UPDATE logs SET status = ? WHERE id = ?"
        self.db_helper.execute_query(update_query, (status, log_id))

    def delete_log(self, log_id):
        delete_query = "DELETE FROM logs WHERE id = ?"
        self.db_helper.execute_query(delete_query, (log_id,))

    def __del__(self):
        self.db_helper.close_connection()
