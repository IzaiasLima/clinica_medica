import connection

print(f"Script {__name__} executado.")


def drop_tables():
    """Excluir as tabelas"""

    con, cur = connection.get()

    try:
        cur.execute("DROP TABLE medicos")
        cur.execute("DROP TABLE pacientes")
    except:
        pass

    con.commit()
    con.close()


def tbl_create():
    """Criar as tabelas MEDICOS e PACIENTES."""

    con, cur = connection.get()

    PRIMARY_KEY = (
        "id SERIAL NOT NULL PRIMARY KEY"
        if connection.DB_TYPE == connection.TYPE_PSQL
        else "id integer PRIMARY KEY AUTOINCREMENT"
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS medicos
            (   {PRIMARY_KEY},
                nome varchar(150),
                rg varchar(15),
                cpf varchar(14),
                dt_nasc date,
                sexo varchar(15),
                uf varchar(2),
                cidade varchar(50),
                cep varchar(9),
                logradouro varchar(150),
                crm varchar(9),
                email varchar(100),
                telefone varchar(15),
                especialidade varchar(50),
                turno varchar(30),
                status varchar(30)
            )
        """
    )

    cur.execute(
        f"""
            CREATE TABLE IF NOT EXISTS pacientes
            (   {PRIMARY_KEY},
                nome varchar(150),
                rg varchar(15),
                cpf varchar(14),
                dt_nasc date,
                sexo varchar(15),
                peso integer,
                altura integer,
                tp_sanguineo varchar(3),
                uf varchar(2),
                cidade varchar(50),
                cep varchar(9),
                logradouro varchar(150),
                email varchar(100),
                telefone varchar(15),
                status varchar(30)
            )
        """
    )

    con.commit()
    con.close()

    print("Tabelas criadas.")


def tables_init():
    """Incluir dados iniciais de teste nas tabelas."""

    con, cur = connection.get()

    medicos = [
        (
            "Natanael Monteiro",
            "123456/SSP-PA",
            "789.456.123-99",
            "1994-07-28",
            "masculino",
            "DF",
            "Águas Claras",
            "71909-540",
            "Rua 12 Norte, lote 6, Apto 904",
            "123456/DF",
            "natan@gmail.com",
            "(61) 98181-3390",
            "cardiologista",
            "diurno",
            "ativo",
        ),
    ]

    pacientes = [
        (
            "Dileyciane Monteiro",
            "RG 23456/SSP-PA",
            "123.456.789-10",
            "1974-06-28",
            "feminino",
            53,
            161,
            "AB+",
            "PA",
            "Santa Maria do Pará",
            "68700-000",
            "Av. Bernardo Sayão, 2345",
            "ciane@gmail.COM",
            "(91) 98888-7654",
            "Agendada",
        ),
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")

    ## FIX: Resolver com Strategy, futuramente
    if connection.DB_TYPE == connection.TYPE_PSQL:
        cur.executemany(
            "INSERT INTO medicos VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            medicos,
        )
        cur.executemany(
            "INSERT INTO pacientes VALUES (DEFAULT,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            pacientes,
        )
    else:
        cur.executemany(
            "INSERT INTO medicos VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", medicos
        )
        cur.executemany(
            "INSERT INTO pacientes VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            pacientes,
        )

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    drop_tables()
    tbl_create()
    tables_init()
