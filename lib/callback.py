from helpers.database.sqlite_helper import SQLiteHelper
from helpers.config_helper import config
from datetime import datetime
import requests

class Log:
    good = 0
    notGood = 0
    def __init__(self, db_name="assets/databases/log.db"):
        self.db_helper = SQLiteHelper(db_name)
        self.db_helper.connect()
        self.create_log_table()
        datas = self.get_logs()
        for data in datas:
            if(data[2] == "1"):
                self.good+=1
            if(data[2] == "0"):
                self.notGood+=1

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
        if(status == 1):
            self.good += 1
        if(status == 0):
            self.notGood += 1

    def add_log_server(self):
        datas = self.get_logs()
        for data in datas:
            dt = {'id_machine': config.get('id_machine', '9999'), 'date': data[1], 'status': data[2]}
            response = requests.post(config.get('url_server', 'http://localhost/qc_web/') + 'api/log', data=dt)

            if response.status_code == 201:
                print('Permintaan berhasil!')
            else:
                print('Permintaan gagal:', response.status_code)
            # Melihat isi respon
            print(response.text)

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
