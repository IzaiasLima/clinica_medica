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

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS medicos
            (   id SERIAL NOT NULL PRIMARY KEY,
                nome text,
                crm text,
                email text,
                especialidade text,
                turno text,
                status text
            )
        """
    )

    # id integer PRIMARY KEY AUTOINCREMENT
    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS pacientes
            (   id SERIAL NOT NULL PRIMARY KEY,
                nome text,
                email text,
                telefone text,
                status text
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
            "Kaio de Oliveira",
            "123456",
            "kaio@gmail.com",
            "cardiologia",
            "noturno",
            "ativo",
        ),
        (
            "Dileyciane Monteiro",
            "23456",
            "ciane@gmail.COM",
            "dermatologia",
            "diurno",
            "em análise",
        ),
        (
            "luciana monteiro",
            "4445566",
            "DRA@LUCIANA.COM",
            "dermatologia",
            "noturno",
            "ativo",
        ),
    ]

    pacientes = [
        ("Natanael Monteiro", "natan@gmail.com", "61 98181-3390", "internado"),
        ("Izaias lima", "izaias@gmail.com", "61 98180-3090", "atendido"),
        ("Luciete lima", "luciete@gmail.com", "61 98180-3090", "atendido"),
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")

    ## FIX: Resolver com Strategy, futuramente
    if connection.DB_TYPE == "psql":
        cur.executemany(
            "INSERT INTO medicos VALUES (DEFAULT,%s,%s,%s,%s,%s,%s)", medicos
        )
        cur.executemany("INSERT INTO pacientes VALUES (DEFAULT,%s,%s,%s,%s)", pacientes)
    else:
        cur.executemany("INSERT INTO medicos VALUES (NULL,?,?,?,?,?,?)", medicos)
        cur.executemany("INSERT INTO pacientes VALUES (NULL,?,?,?,?)", pacientes)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    drop_tables()
    tbl_create()
    tables_init()
