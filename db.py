import sqlite3 as s

con = s.connect("clinica.db")
con.row_factory = s.Row
cur = con.cursor()


def get_pacientes():
    return get_dados("pacientes")


def get_paciente(id):
    return get_dados("pacientes", id)


def add_paciente(new_paciente):
    add("pacientes", new_paciente)


def update_paciente(id, updated):
    paciente = get_paciente(id)
    update(id, "pacientes", paciente, updated)


def del_paciente(id):
    delete("pacientes", id)


def get_medicos():
    return get_dados("medicos")


def get_medico(id):
    return get_dados("medicos", id)


def add_medico(new_medico):
    add("medicos", new_medico)


def update_medico(id, updated):
    medico = get_medico(id)
    update(id, "medicos", medico, updated)


def del_medico(id):
    delete("medicos", id)


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    rows = cur.execute(sql).fetchall()
    dados = [dict(row) for row in rows]
    return dados


def add(table, dados: dict):
    if dados:
        values = [f"'{v}'" for _, v in dados.items()]
        all_values = ",".join(values)

        sql = f"INSERT INTO {table} values (NULL, {all_values})"
        cur.execute(sql)
        con.commit()


def update(id, table, outdated: dict, updated: dict):
    if outdated:
        dados = outdated[0]
        dados.update(updated)

        fields = [f"{k}='{v}'" for k, v in dados.items()]
        all_fields = ",".join(fields)

        sql = f"UPDATE {table} SET {all_fields} WHERE id={id}"
        cur.execute(sql)
        con.commit()


def delete(tbl, id):
    sql = f"DELETE FROM {tbl} WHERE id={id}"
    cur.execute(sql)
    con.commit()
