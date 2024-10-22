import sqlite3

import psycopg2
import psycopg2.extras

TYPE_PSQL = "psql"
TYPE_SQLITE = "sqlite"
TYPE_MYSQL = "mysql"

DB_TYPE = TYPE_PSQL


def get():
    if DB_TYPE == TYPE_PSQL:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
        )
        cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return con, cur

    elif DB_TYPE == TYPE_SQLITE:
        con = sqlite3.connect("clinica.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return con, cur

    elif DB_TYPE == TYPE_MYSQL:
        raise NotImplementedError("Conexão com o MySql não implementada.")

    else:
        raise NotImplementedError("Tipo de DB desconhecido.")
