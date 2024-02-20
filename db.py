import sqlite3 as s

con = s.connect("clinica.db")
con.row_factory = s.Row
cur = con.cursor()


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    rows = cur.execute(sql).fetchall()
    dados = [dict(row) for row in rows]
    return dados


def get_medicos():
    return get_dados("medicos")


def del_medico(id):
    delete("medicos", id)


def get_pacientes():
    return get_dados("pacientes")


def get_paciente(id):
    return get_dados("pacientes", id)


def update_paciente(id, updated: dict):
    paciente = get_paciente(id)

    if paciente:
        dados = paciente[0]
        dados.update(updated)

        fields = [f"{k}='{v}'" for k, v in dados.items()]
        all_fields = ",".join(fields)

        sql = f"UPDATE pacientes SET {all_fields} WHERE id={id}"
        cur.execute(sql)
        con.commit()
    return


def del_paciente(id):
    delete("pacientes", id)


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
    return
