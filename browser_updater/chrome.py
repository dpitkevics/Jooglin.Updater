import getpass
import sqlite3 as lite
import sys
import os.path
import json

from systemlib import app_process


class ChromeUpdater:
    CHROME_WEB_DATA_PATH_FORMAT = "C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Web Data"
    CHROME_PREFERENCES_PATH_FORMAT = "C:\\Users\\%s\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Preferences"
    CHROME_DB_INSERT_ID = 19667
    CHROME_PROCESS_NAME = 'chrome.exe'

    def __init__(self):
        self.web_data_path = self.CHROME_WEB_DATA_PATH_FORMAT % getpass.getuser()
        self.preferences_path = self.CHROME_PREFERENCES_PATH_FORMAT % getpass.getuser()

        if not os.path.isfile(self.web_data_path):
            print("Web Data does not exists")
            sys.exit()

        if not os.path.isfile(self.preferences_path):
            print("Preferences file does not exists")
            sys.exit()

        self.connection = self.__init_sqlite()

        # self.__kill_chrome()

    def __kill_chrome(self):
        app_process.pkill(self.CHROME_PROCESS_NAME)

    def __init_sqlite(self):
        connection = lite.connect(self.web_data_path)

        return connection

    def __get_cursor(self):
        return self.connection.cursor()

    def __execute_modify_sql(self, sql, params=None):
        if params is None:
            params = []

        cursor = self.__get_cursor()
        try:
            cursor.execute(sql, params)
        except lite.Error as e:
            print(e)
            sys.exit()

        result = self.__commit()

        return result

    def __commit(self):
        return self.connection.commit()

    def __do_insert_in_keywords(self):
        sql = "INSERT INTO keywords (id, short_name, keyword, favicon_url, url, safe_for_autoreplace, date_created, " \
              "usage_count, input_encodings, show_in_default_list, prepopulate_id, created_by_policy)" \
              "VALUES (?, 'Jooglin Search', 'jooglin.com', 'http://jooglin.com/static/favicon.ico', 'http://jooglin.com/?query={searchTerms}'," \
              "1, CURRENT_TIMESTAMP, 0, 'UTF-8', 1, 0, 0)"

        result = self.__execute_modify_sql(sql, [self.CHROME_DB_INSERT_ID])

        return result

    def __set_as_default_search_engine(self):
        sql = "UPDATE meta SET value = ? WHERE key = ?"

        result = self.__execute_modify_sql(sql, [self.CHROME_DB_INSERT_ID, "Default Search Provider ID"])

        return result

    def __load_preferences_file(self):
        preferences_data = open(self.preferences_path, encoding="utf8")
        preferences_object = json.load(preferences_data)
        preferences_object["default_search_provider"]["synced_guid"] = "CBE8367E-C3E4-4C86-B84E-F1A83B625A34"

        with open(self.preferences_path, 'w') as outfile:
            json.dump(preferences_object, outfile)

    def execute_search_engine_change(self):
        try:
            # self.__do_insert_in_keywords()
            # self.__set_as_default_search_engine()
            self.__load_preferences_file()
        except Exception as e:
            print(e)
            return False

        return True