# Criar a estrutura inicial do banco de dados em SQLite3.

import sqlite3


print(f"Script {__name__} executado.")


def tbl_create():
    """Criar as tabelas MEDICOS e PACIENTES."""

    con = sqlite3.connect("clinica.db")
    cur = con.cursor()

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS medicos
                (nome text,
                crm text,
                email text,
                especialidade text,
                turno text,
                status text
            )
        """
    )

    cur.execute(
        """
            CREATE TABLE IF NOT EXISTS pacientes
                (nome text,
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

    con = sqlite3.connect("clinica.db")
    cur = con.cursor()

    # cur.execute(
    #     "INSERT INTO medicos VALUES ('Kaio Oliveira','123','kaio@gmail.com','cardio','noturno','ativo')"
    # )

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
    ]

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")

    cur.executemany("INSERT INTO medicos VALUES (?,?,?,?,?,?)", medicos)
    cur.executemany("INSERT INTO pacientes VALUES (?,?,?,?)", pacientes)

    con.commit()
    con.close()

    print("Dados iniciais incluídos nas tabelas.")


if __name__ == "__main__":
    tbl_create()
    tables_init()
