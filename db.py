import sqlite3 as sql

con = sql.connect(
    "clinica.db",
)
con.row_factory = sql.Row
cur = con.cursor()


def get_medicos():
    # return None
    return get_dados("medicos")


def get_pacientes():
    return get_dados("pacientes")


def get_dados(tbl):
    sql = f"SELECT * FROM {tbl}"
    rows = cur.execute(sql).fetchall()
    dados = [dict(row) for row in rows]
    return dados


def del_medico(id):
    delete("medicos", id)


def del_paciente(id):
    delete("pacientes", id)


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
    return
