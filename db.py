import bcrypt

import connection

TBL_MEDICOS = "medicos"
TBL_PACIENTES = "pacientes"
TBL_CONSULTAS = "consultas"
TBL_USUARIOS = "usuarios"

con, cur = connection.get()


def get_usuarios():
    return get_dados(TBL_USUARIOS)


def is_usuario(body):
    senha = str.encode(body["senha"])
    dados = get_usuario(TBL_USUARIOS, body)
    if dados:
        senha_crypt = str.encode(dados[0]["senha"])
        return bcrypt.checkpw(senha, senha_crypt)
    else:
        return False


def get_usuario(tbl, dados):
    if dados:
        values = [v for _, v in dados.items()]
        usuario = values[0]

        sql = f"SELECT * FROM {tbl}"
        sql += f" WHERE usuario='{usuario}'"

        cur.execute(sql)
        rows = cur.fetchall()
        dados = [dict(row) for row in rows]

        return dados
    else:
        return {}


def get_pacientes():
    return get_dados(TBL_PACIENTES)


def get_pacientes_paged(len_page, page=0):
    dados = get_dados_paged(TBL_PACIENTES, len_page, page)
    dados.update(pagination(TBL_PACIENTES, len_page, page))
    return dados


def get_paciente_position(nome, len_page):
    page = get_page(TBL_PACIENTES, nome, len_page)
    dados = get_pacientes_paged(len_page, page)
    return dados


def get_paciente(id):
    return get_dados(TBL_PACIENTES, id)


def add_paciente(new_paciente):
    add(TBL_PACIENTES, new_paciente)


def update_paciente(id, updated):
    paciente = get_paciente(id)
    update(id, TBL_PACIENTES, paciente, updated)


def del_paciente(id):
    delete(TBL_PACIENTES, id)


def get_medicos():
    return get_dados(TBL_MEDICOS)


def get_medicos_paged(len_page, page=0):
    dados = get_dados_paged(TBL_MEDICOS, len_page, page)
    dados.update(pagination(TBL_MEDICOS, len_page, page))
    return dados


def get_medicos_ativos(page=0):
    len_page = 3
    dados = get_dados_paged(TBL_MEDICOS, len_page, page, status="ativo")
    dados.update(pagination(TBL_MEDICOS, len_page, page))
    return dados


def get_medico_position(nome, len_page):
    page = get_page(TBL_MEDICOS, nome, len_page)
    dados = get_medicos_paged(len_page, page)
    return dados


def get_medico(id):
    return get_dados(TBL_MEDICOS, id)


def add_medico(new_medico: dict):
    add(TBL_MEDICOS, new_medico)


def update_medico(id, updated):
    medico = get_medico(id)
    update(id, TBL_MEDICOS, medico, updated)


def del_medico(id):
    delete(TBL_MEDICOS, id)


def get_consultas(tp_order=0, is_agendadas=False):
    return get_dados_consultas(tp_order, is_agendadas)


def add_consulta(new_consulta):
    add(TBL_CONSULTAS, new_consulta)


def close_consulta(id):
    set_status(TBL_CONSULTAS, "concluída", id)


def del_consulta(id):
    set_status(TBL_CONSULTAS, "cancelada", id)


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    sql += " ORDER BY nome"

    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]

    return dados


def get_dados_paged(tbl, len_page=0, page=-1, status=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE status = '{status}'" if status else ""
    sql += f" ORDER BY nome"
    sql += f" LIMIT {len_page} OFFSET {page * len_page}" if page >= 0 else ""
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dict({"info": dados})


def search_medicos(param):
    dados = search(TBL_MEDICOS, param)
    dados.update(pagination(TBL_MEDICOS))
    return dados


def search_pacientes(param):
    return search(TBL_PACIENTES, param)


def search(tbl, param):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE UPPER(nome) LIKE '%{param.upper()}%'"
    sql += f" OR cpf LIKE '{param}%'"
    sql += " ORDER BY nome"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dict({"info": dados})


def get_dados_consultas(tp_order=0, is_agendadas=False, id=None):
    ORDER = [
        "p.nome, dt_consulta, hr_consulta",
        "nm_medico, status, dt_consulta, hr_consulta",
        "dt_consulta desc, hr_consulta, nm_medico",
        "status, dt_consulta, hr_consulta, p.nome",
    ]

    sql = "SELECT c.*, m.nome AS nm_medico, m.especialidade, p.nome AS nm_paciente, p.telefone"
    sql += " FROM consultas AS c"
    sql += " INNER JOIN medicos AS m ON (m.id = c.id_medico)"
    sql += " INNER JOIN pacientes AS p ON (p.id = c.id_paciente)"
    sql += f" WHERE id={id}" if id else ""
    sql += f" AND c.status='agendada'" if is_agendadas else ""
    sql += f" ORDER BY {ORDER[tp_order]}"

    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]

    return dados


def get_id_consulta(id_medico, dt_consulta, hr_consulta):
    sql = f"SELECT id FROM {TBL_CONSULTAS}"
    sql += f" WHERE id_medico = {id_medico}"
    sql += f" AND dt_consulta = '{dt_consulta}'"
    sql += f" AND hr_consulta = '{hr_consulta}'"

    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]

    return dados


def consultas_por_medico():
    sql = f"SELECT nome, COUNT(*) AS qtd FROM {TBL_CONSULTAS} AS c"
    sql += f" INNER JOIN {TBL_MEDICOS} AS m ON (c.id_medico=m.id)"
    sql += " WHERE c.status = 'concluída'"
    sql += " GROUP BY m.id"

    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def consultas_por_mes():
    import mes

    sql = None

    if connection.DB_TYPE == connection.TYPE_PSQL:
        sql = "SELECT CAST(to_char(dt_consulta, 'mm') AS INT) AS mes, COUNT(*) AS qtd"
    elif connection.DB_TYPE == connection.TYPE_SQLITE:
        sql = "SELECT CAST(strftime('%m', dt_consulta) AS INT) AS mes, COUNT(*) AS qtd "
    else:
        raise NotImplementedError("Tipo de Banco de Dados desconhecido.")

    sql += f" FROM {TBL_CONSULTAS} WHERE status='concluída' GROUP BY mes"

    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    [d.update({"mes": mes.to_str(d.get("mes"))}) for d in dados]
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


def set_status(tbl, status, id):
    sql = f"UPDATE {tbl} SET status='{status}' WHERE id={id}"
    cur.execute(sql)
    con.commit()


def delete(tbl, id):
    try:
        sql = f"DELETE FROM {tbl} WHERE id={id}"
        cur.execute(sql)
        con.commit()
    except Exception as exc:
        con.rollback()
        raise exc


def count(tbl):
    sql = f"SELECT COUNT(*) AS total FROM {tbl}"
    cur.execute(sql)
    return cur.fetchone()["total"]


def get_page(tbl, nome, len_page):
    sql = f"SELECT COUNT(*) as total FROM {tbl} WHERE UPPER(nome) < '{nome}'"
    cur.execute(sql)
    position = cur.fetchone()["total"]
    return position // len_page


def pagination(tbl, len_page=0, page=0):
    total_rows = count(tbl) - 1
    total_pages = (total_rows // len_page) if len_page > 0 else 0

    if total_pages > 0:
        pages = {
            "this_page": page,
            "pagination": {
                "first_page": page == 0,
                "alias_first_page": "first_page" if page == 0 else "",
                "previous_page": page - 1 if page > 1 else 0,
                "next_page": page + 1 if page < total_pages else page,
                "alias_last_page": "last_page" if page >= total_pages else "",
                "last_page": page >= total_pages,
                "total_pages": total_pages,
            },
        }
    else:
        pages = {"this_page": page}

    return pages
