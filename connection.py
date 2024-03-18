import sqlite3

import psycopg2
import psycopg2.extras

DB_TYPE = "psql"


def get():
    ## FIX: Resolver com Strategy, futuramente
    if DB_TYPE == "psql":

        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="192.168.1.12",
            port="5432",
        )
        cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        return con, cur

    elif DB_TYPE == "mysql":
        raise NotImplementedError("Conexão com o MySql não implementada.")

    else:
        con = sqlite3.connect("clinica.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        return con, cur
