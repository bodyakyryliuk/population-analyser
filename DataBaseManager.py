import json
import os
import sqlite3
import kaggle


def download_and_extract_json(dataset_name):
    os.environ["KAGGLE_CONFIG_DIR"] = r"C:\Users\bodkr\.kaggle"

    kaggle.api.dataset_download_files(dataset_name, unzip=True)

    with open("data.json") as json_file:
        data = json.load(json_file)
        return data


def get_column_names(data):
    column_names = set()

    def extract_keys(obj):
        if isinstance(obj, dict):
            column_names.update(obj.keys())
            for value in obj.values():
                extract_keys(value)
        elif isinstance(obj, list):
            for item in obj:
                extract_keys(item)

    extract_keys(data)
    return column_names


class DataBaseManager:
    connection = sqlite3.connect('database.db')

    def __init__(self, table_name, main_window):
        self.json_data = download_and_extract_json("rajkumarpandey02/2023-world-population-by-country")
        self.columns = list(get_column_names(self.json_data))
        self.main_window = main_window
        self.table_name = table_name
        self.create_table()
        self.insert_data()

    def create_table(self):
        columns_with_types = ', '.join(f'{column} TEXT' for column in self.columns)
        create_table_query = f'CREATE TABLE IF NOT EXISTS {self.table_name} ({columns_with_types})'
        cursor = self.connection.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name}")
        cursor.execute(create_table_query)

    def insert_data(self):
        cursor = self.connection.cursor()

        def insert_rows(obj):
            if isinstance(obj, dict):
                values = [obj.get(column, '') for column in self.columns]
                cursor.execute(f'INSERT INTO {self.table_name} VALUES ({",".join(["?"] * len(self.columns))})', values)
            elif isinstance(obj, list):
                for item in obj:
                    insert_rows(item)

        insert_rows(self.json_data)
        self.connection.commit()

    def select_countries(self):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT country FROM {self.table_name}")
        countries = []
        rows = cursor.fetchall()
        for row in rows:
            countries.append(row[0])

        return countries

    def select_all_data(self, table_name):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        return rows

    def get_plot_dict(self, country):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT pop1980,pop2000,pop2010,pop2022,pop2023,pop2030,pop2050 "
                       f"FROM {self.table_name} WHERE country = ?", (country,))
        row = cursor.fetchone()
        data_dict = {}

        if row is not None:
            column_names = [1980, 2000, 2010, 2022, 2023, 2030, 2050]

            for i, column in enumerate(column_names):
                value = row[i]
                if value.isdigit():
                    data_dict[column] = int(value)
                else:
                    data_dict[column] = float(value)
        return data_dict

    def get_general_plot_dict(self, year):
        cursor = self.connection.cursor()
        cursor.execute(f"SELECT country, pop{year} FROM {self.table_name}")
        rows = cursor.fetchall()
        data_dict = {row[0]: row[1] for row in rows}
        print(data_dict)

        return data_dict

    def delete_table(self):
        if not self.main_window.create_confirmation_window("Do you want to clear the database?"):
            self.main_window.update_status_line("Database clearing operation was declined!")
            return

        cursor = self.connection.cursor()

        # Execute the DROP TABLE statement
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")

        for object in self.main_window.get_objects():
            object.configure(state="disabled")

        self.main_window.update_status_line("Database is cleared successfully!")
        # Commit the changes and close the connection
        self.connection.commit()

    def fill_db(self):
        self.create_table()
        self.insert_data()

        for object in self.main_window.get_objects():
            object.configure(state="normal")

    def get_connection_cursor(self):
        return self.connection.cursor()

