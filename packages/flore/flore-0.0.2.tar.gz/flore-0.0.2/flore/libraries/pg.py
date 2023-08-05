import psycopg2

from flore.libraries.base import Base
from flore.table import compose


class Postgres(Base):
    def __init__(self, config: dict, tables: dict) -> None:
        self.host = config["host"]
        self.user = config["username"]
        self.password = config["password"]
        self.dbname = config["database"]
        self.port = config["port"]
        self.conn = None
        self.tables = tables

    def open(self):
        """ open connection with postgres """

        conn_string = f"host={self.host} user={self.user} password={self.password} dbname={self.dbname} port={self.port}"
        try:
            self.conn = psycopg2.connect(conn_string)
            print("POSTGRES::Connection established")
        except Exception as e:
            print(str(e))

    def create(self):
        """ create tables in postgres database """

        parse = ""

        for table_name, columns in self.tables.items():
            parse += compose(table_name, columns)
        if self.conn:
            cursor = self.conn.cursor()
            cursor.execute(parse)

            # commit to database
            try:
                self.conn.commit()
                print(
                    "WOW...We were able to create your tables in the database."
                )
            except Exception:
                self.conn.rollback()
                print(
                    "WOW...We were able to create your tables in the database."
                )

            # close connection
            cursor.close()
            self.conn.close()
