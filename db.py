import connection

TBL_MEDICOS = "medicos"
TBL_PACIENTES = "pacientes"

con, cur = connection.get()


def get_pacientes():
    return get_dados(TBL_PACIENTES)


def get_paciente(id):
    return get_dados(TBL_PACIENTES, id)


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


def get_medicos_position(nome, len_page):
    page = get_position(TBL_MEDICOS, nome, len_page)
    dados = get_dados_paged(TBL_MEDICOS, len_page, page)
    dados.update(pagination(TBL_MEDICOS, len_page, page))
    return dados


def get_medico(id):
    return get_dados(TBL_MEDICOS, id)


def add_medico(new_medico: dict):
    dados = {
        "logradouro": "Rua Doze, 6",
        "cep": "71900-999",
        "cidade": "Brasília",
        "uf": "df",
    }
    new_medico.update(dados)

    add(TBL_MEDICOS, new_medico)

    # names = get_names()
    # for name in names:
    #     new_medico.update({"nome": name})
    #     add(TBL_MEDICOS, new_medico)


def update_medico(id, updated):
    medico = get_medico(id)
    update(id, TBL_MEDICOS, medico, updated)


def del_medico(id):
    delete(TBL_MEDICOS, id)


def get_dados(tbl, id=None):
    sql = f"SELECT * FROM {tbl}"
    sql += f" WHERE id={id}" if id else ""
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dados


def get_dados_paged(tbl, len_page=0, page=-1):
    sql = f"SELECT * FROM {tbl} ORDER BY 2"
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
    sql += " ORDER BY 2"
    cur.execute(sql)
    rows = cur.fetchall()
    dados = [dict(row) for row in rows]
    return dict({"info": dados})


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


def count(tbl):
    sql = f"SELECT COUNT(*) AS total FROM {tbl}"
    cur.execute(sql)
    return cur.fetchone()["total"]


def get_position(tbl, nome, len_page):
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
                "page": page,
                "next_page": page + 1 if page < total_pages else page,
                "alias_last_page": "last_page" if page >= total_pages else "",
                "last_page": page >= total_pages,
                "total_pages": total_pages,
            },
        }
    else:
        pages = {"this_page": page}

    return pages


def get_names():
    return [
        "Cleuza Ferreira",
        "Inácio Danilo Chaves",
        "Paula Feliciano Frias",
        "Patrícia Benites de Guimarães",
        "Célia Mayara Esteves",
        "Felipe Chaves",
        "Samanta Aguiar Bittencourt",
        "José Faria de Gomes",
        "Liane Rosimeire Carmona",
        "Ali Ortiz Filho",
        "Elói Aguiar Sobrinho",
        "Everaldo Michel Branco",
        "João Gomes de Madureira",
        "Fabíola Aragão Furtado",
        "Madalena Vitória Dias Ortega",
        "Luara Casanova da Lira",
        "Karina Michele Escobar",
        "Lena Tatiana Assunção",
        "Pedro Walter Azevedo",
        "João Ferreira de Almeida",
        "Cícero Lino Caldeira",
        "Meire Dias de Reis",
        "Renata Tatiana de Lutero",
        "Isabella Aguiar Lozano",
        "Irene Clarice Corona",
        "Ivone Corona",
        "Fernando Willian Guerra",
        "Áureo de Mascarenhas Filho",
        "Camilo Batista de Pinheiro",
        "Ricardo de Rocha Filho",
        "Batista Gil de Mendonça",
        "Mike Ramon Feliciano Filho",
        "Batista Santana de Solano",
        "Joaquin Manoel de Arruda",
        "Bartolomeu Ferreira da Silva",
        "Sérgio Fábio de Meireles",
        "Anderson Wilson Aguiar Jardim",
        "Aaron Everton Faria de Paes",
        "Eric Ivan de Branco Neto",
        "Gustavo Sales",
        "Adílson Carmona",
        "Kevin Batista Flores de Rosa",
        "Cristiano Padilha Câmara",
        "Felipe Casanova",
        "Benjamin Luan Aranda",
        "Helder Inácio de Uchoa",
        "Cícero Jardel Casanova",
        "Christian Hélio de Garcia",
        "Amarildo Lucas de Sobrinho",
        "Simão Otaviano de Faria",
        "Tomás Matias de Sanches",
    ]
