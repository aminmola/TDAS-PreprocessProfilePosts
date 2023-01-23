import mysql.connector
from typing import List
import utils.config as cfg
from utils.logger import Logger
from mysql.connector import Error

log = Logger('utils')


class MySQL(object):
    """
    mysql connection
    """

    def __init__(self, db_name: str, host: str = None):
        """
        Initialize MySQL class
        """
        self._host = host
        self._connection = None
        self.database_name = db_name

    def __enter__(self):
        """
        Open mysql connection
        """
        try:
            if self._host is None:
                self._host = cfg.MYSQL_GENERAL_HOST
            self._connection = mysql.connector.connect(host=self._host,
                                                       database=self.database_name,
                                                       user=cfg.MYSQL_GENERAL_USERNAME,
                                                       password=cfg.MYSQL_GENERAL_PASSWORD)

            return self
        except Exception as e:
            log.error(f"Can not connect to mysql, {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close MySQL connection
        """
        try:
            self._connection.close()
        except Exception as e:
            log.error(f"MySQL close connection failed, {e}")

    def execute(self, query: str) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            cursor.close()
            self._connection.commit()
            return True
        except Exception as e:
            log.error(f"MySQL execute query failed, {e}")
            return False

    def read(self, query):
        try:
            out = []
            cursor = self._connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            columns = [i[0] for i in cursor.description]
            cursor.close()
            self._connection.commit()
            for r in records:
                record = {}
                for i, item in enumerate(r):
                    record.update({columns[i]: item})
                out.append(record)
            return out
        except Exception as e:
            log.error(f"MySQL execute query failed, {e}")
            return None

    def insert(self, table: str, record: dict or List[dict]) -> bool:
        """
        Insert record in table
        """
        try:
            if type(record) == dict:
                fields = ",".join(record.keys())
                values = tuple(record.values())
                query = f"INSERT INTO {table} ({fields}) VALUES {values}"
                if len(values) == 1:
                    query = query.replace(",", "")
                cursor = self._connection.cursor()
                cursor.execute(query)
                cursor.close()
                self._connection.commit()
                return True
            elif type(record) == list:
                records_list_template = ','.join(['%s'] * len(record))
                values = []
                fields = ", ".join(record[0].keys())
                for d in record:
                    values.append(tuple(d.values()))
                insert_query = f'insert into {table} ({fields}) values {records_list_template}'
                cursor = self._connection.cursor()
                cursor.execute(insert_query, values)
                cursor.close()
                self._connection.commit()
                return True
            else:
                raise ValueError('invalid input type')
        except Exception as e:
            print(f"Insert {table} failed, {e}")
            return False

    def update(self, table: str, record: dict or List[dict], condition: str) -> bool:
        """
        Update record in table
        """
        try:
            if type(record) == dict:
                field_values = []
                for field, value in record.items():
                    if isinstance(value, str):
                        value = f"'{value}'"
                    field_values.append(f"{field}={value}")
                query = f"UPDATE {table} SET {','.join(field_values)} WHERE {condition}"
                cursor = self._connection.cursor()
                cursor.execute(query)
                cursor.close()
                self._connection.commit()
            elif type(record) == list:
                field_values = []
                for r in record:
                    for field, value in record.items():
                        if isinstance(value, str):
                            value = f"'{value}'"
                        field_values.append(f"{field}={value}")
                query = f"UPDATE {table} SET {','.join(field_values)} WHERE {condition}"
                cursor = self._connection.cursor()
                cursor.execute(query)
                cursor.close()
                self._connection.commit()
            else:
                raise ValueError('invalid input type')
        except Exception as e:
            print(f"Update {table} failed, {e}")
            return False

    def upsert(self, table: str, record: dict or List[dict], condition: str):
        """
        Upsert record in table
        """
        try:
            field_values = []
            for field, value in record.items():
                if isinstance(value, str):
                    value = f"'{value}'"
                field_values.append(f"{field}={value}")
            fields = ",".join(record.keys())
            values = tuple(record.values())
            query = f"""
                    DO $$
                        BEGIN
                            IF EXISTS(SELECT * FROM {table} WHERE {condition}) THEN
                               UPDATE {table} SET {','.join(field_values)} WHERE {condition};
                            ELSE
                               INSERT INTO {table} ({fields}) VALUES {values};
                            END IF;
                        END
                    $$
            """
            cursor = self._connection.cursor()
            cursor.execute(query)
            cursor.close()
            self._connection.commit()
            return True
        except Exception as e:
            print(f"Upsert {table} failed, {e}")
            return False

    def is_exist(self, table: str, condition: str) -> bool:
        """
        Check record exist in MySQL
        """
        try:
            query = f"SELECT * FROM {table} WHERE {condition}"
            cursor = self._connection.cursor(cursor_factory=ext.RealDictCursor)
            cursor.execute(query)
            record = cursor.fetchone()
            cursor.close()
            return record
        except Exception as e:
            print(f"Check is exist record failed, {e}")
