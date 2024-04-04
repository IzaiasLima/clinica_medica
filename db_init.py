import connection
import db

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

    medico = {
        "rg": "3334-44",
        "cpf": "442.456.789-10",
        "dt_nasc": "1987-12-11",
        "sexo": "Feminino",
        "uf": "RJ",
        "cidade": "Brasília",
        "cep": "70277-020",
        "logradouro": "Rua Doze, 6",
        "crm": "432-df",
        "email": "ls@gmail.com",
        "telefone": "(61) 98181-3390",
        "especialidade": "psicanalise",
        "turno": "noturno",
        "status": "inativo",
    }

    paciente = {
        "rg": "1233334/SSP-DF",
        "cpf": "123.456.789-10",
        "dt_nasc": "1970-04-25",
        "sexo": "masculino",
        "uf": "RJ",
        "cidade": "Brasília",
        "cep": "71909-540",
        "logradouro": "Rua Doze, 6",
        "email": "ls@gmail.com",
        "telefone": "(61) 98181-3390",
        "altura": "165",
        "peso": "65",
        "status": "agendada",
    }

    cur.execute("DELETE FROM medicos")
    cur.execute("DELETE FROM pacientes")
    con.commit()

    for name in get_medicos():
        medico.update({"nome": name})
        db.add(db.TBL_MEDICOS, medico)

    for name in get_pacientes():
        paciente.update({"nome": name})
        db.add(db.TBL_PACIENTES, paciente)

    print("Dados iniciais incluídos nas tabelas.")


def get_medicos():
    return [
        "Dileyciane Monteiro",
        "Madalena Vitória Dias Ortega",
        "Luara Casanova da Lira",
        "Karina Michele Escobar",
        "Lena Tatiana Assunção",
        "Helena Clarice Padilha",
        "Renata Tatiana de Lutero",
        "Irene Clarice Corona",
        "Sara Meireles",
        "Cristina Padilha Câmara",
        "Ana Carolina Jardel Casanova",
        "Vitória Sanches",
    ]


def get_pacientes():
    return [
        "Natanael Monteiro",
        "Inácio Danilo Chaves",
        "Paulo Feliciano Frias",
        "Patrônio Benites de Guimarães",
        "Celso Mauro Esteves",
        "Felipe Chaves",
        "José Faria de Gomes",
        "Luiz Rosário de Carmona",
        "Ali Ortiz Filho",
        "Elói Aguiar Sobrinho",
        "Everaldo Michel Branco",
        "João Gomes de Madureira",
        "Fábio Aragão Furtado",
        "Marcos Vitor Dias Ortega",
        "Kaio Michael Escobar",
        "Leandro Toledo Assunção",
        "Pedro Walter Azevedo",
        "João Ferreira de Almeida",
        "Cícero Lino Caldeira",
        "Meire Dias de Reis",
        "Renato Tomás de Lutero",
        "Fernando Willian Guerra",
        "Camilo Batista de Pinheiro",
        "Ricardo de Rocha Filho",
        "Mike Ramon Feliciano Filho",
        "Joaquim Manoel de Arruda",
        "Bartolomeu Ferreira da Silva",
        "Sérgio Fábio de Meireles",
        "Anderson Wilson Aguiar Jardim",
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


if __name__ == "__main__":
    drop_tables()
    tbl_create()
    tables_init()
