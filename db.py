import sqlite3 as db

con = db.connect("clinica.db")
cur = con.cursor()


def get_medicos():
    return get_dados("medicos")


def get_pacientes():
    return get_dados("pacientes")


def get_dados(tbl):
    sql = f"SELECT * FROM {tbl}"
    dados = cur.execute(sql).fetchall()
    return dados
