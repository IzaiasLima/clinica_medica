import connection

con, cur = connection.get()


def get_pacientes():
    return get_dados("pacientes")


def get_paciente(id):
    return get_dados("pacientes", id)


def add_paciente(new_paciente):
    dados = {
        "rg": "123",
        "dt_nasc": "2024-06-02",
        "logradouro": "Rua Doze, 6",
        "cep": "71900-999",
        "cidade": "Brasília",
        "uf": "df",
        "sexo": "masculino",
        "tp_sanguineo": "A+",
        "altura": 165,
        "peso": 61,
    }
    new_paciente.update(dados)
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


def add_medico(new_medico: dict):
    dados = {
        "rg": "123",
        "dt_nasc": "2024-06-02",
        "logradouro": "Rua Doze, 6",
        "cep": "71900-999",
        "cidade": "Brasília",
        "uf": "df",
        "sexo": "masculino",
    }
    new_medico.update(dados)

    add("medicos", new_medico)


def update_medico(id, updated):
    medico = get_medico(id)
    update(id, "medicos", medico, updated)


def del_medico(id):
    delete("medicos", id)


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def search_medicos(nome):
    return search("medicos", nome)


def search_pacientes(nome):
    return search("pacientes", nome)


def search(tbl, nome):

    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE UPPER(nome) LIKE '%{nome.upper()}%'"
    sql += f" OR cpf LIKE '{nome}%'"
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def add(table, dados: dict):
    if dados:
        values = [f"'{v}'" for _, v in dados.items()]
        all_values = ",".join(values)

        fields = [f"{k}" for k, _ in dados.items()]
        all_fields = ",".join(fields)

        if connection.DB_TYPE == connection.TYPE_PSQL:
            sql = (
                f"INSERT INTO {table} (id, {all_fields}) values (DEFAULT, {all_values})"
            )
        else:
            sql = f"INSERT INTO {table} (id, {all_fields}) values (NULL, {all_values})"

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
