from contextlib import closing

import psycopg2


def conectar():
    return psycopg2.connect(
        host="localhost",
        database="hotelaria",
        user="postgres",
        password="Arakida",
        port="5432",
    )


def listar_hospedes(cursor):
    cursor.execute("""
        SELECT cpf, nome, email, telefone
        FROM Hospedes
        ORDER BY nome;
    """)
    return cursor.fetchall()


def listar_quartos(cursor):
    cursor.execute("""
        SELECT numero, tipo, capacidade, preco_diaria
        FROM Quartos
        ORDER BY numero;
    """)
    return cursor.fetchall()


def listar_reservas(cursor):
    """Lista as reservas com os dados do hospede e do quarto."""
    cursor.execute("""
        SELECT r.id_reserva, h.cpf, h.nome, q.numero, q.tipo, q.preco_diaria
        FROM Reservas r
        JOIN Hospedes h ON h.cpf = r.cpf_hospede
        JOIN Quartos q ON q.numero = r.numero_quarto
        ORDER BY r.id_reserva;
    """)
    return cursor.fetchall()


def buscar_hospede(cursor, cpf):
    cursor.execute("""
        SELECT cpf, nome, email, telefone
        FROM Hospedes
        WHERE cpf = %s;
    """, (cpf,))
    return cursor.fetchone()


def buscar_quarto(cursor, numero):
    cursor.execute("""
        SELECT numero, tipo, capacidade, preco_diaria
        FROM Quartos
        WHERE numero = %s;
    """, (numero,))
    return cursor.fetchone()


def buscar_reserva(cursor, id_reserva):
    cursor.execute("""
        SELECT id_reserva, cpf_hospede, numero_quarto
        FROM Reservas
        WHERE id_reserva = %s;
    """, (id_reserva,))
    return cursor.fetchone()


def listar_reservas_por_hospede(cursor, cpf):
    cursor.execute("""
        SELECT id_reserva, numero_quarto
        FROM Reservas
        WHERE cpf_hospede = %s
        ORDER BY id_reserva;
    """, (cpf,))
    return cursor.fetchall()


def listar_reservas_por_quarto(cursor, numero):
    cursor.execute("""
        SELECT id_reserva, cpf_hospede
        FROM Reservas
        WHERE numero_quarto = %s
        ORDER BY id_reserva;
    """, (numero,))
    return cursor.fetchall()


def imprimir_registros(titulo, colunas, registros):
    print(f"\n{titulo}")
    if not registros:
        print("  Nenhum registro encontrado.")
        return
    print("  " + " | ".join(colunas))
    for registro in registros:
        print("  " + " | ".join(str(valor) for valor in registro))


def main():
    try:
        with closing(conectar()) as conexao:
            with conexao.cursor() as cursor:
                hospedes = listar_hospedes(cursor)
                quartos = listar_quartos(cursor)
                reservas = listar_reservas(cursor)

                imprimir_registros(
                    "Hóspedes", ["CPF", "Nome", "E-mail", "Telefone"], hospedes
                )
                imprimir_registros(
                    "Quartos",
                    ["Número", "Tipo", "Capacidade", "Preço da diária"],
                    quartos,
                )
                imprimir_registros(
                    "Reservas",
                    [
                        "ID",
                        "CPF",
                        "Hóspede",
                        "Quarto",
                        "Tipo",
                        "Preço da diária",
                    ],
                    reservas,
                )

                if hospedes:
                    cpf = hospedes[0][0]
                    imprimir_registros(
                        f"Reservas do hóspede {cpf}",
                        ["ID", "Quarto"],
                        listar_reservas_por_hospede(cursor, cpf),
                    )
                if quartos:
                    numero = quartos[0][0]
                    imprimir_registros(
                        f"Reservas do quarto {numero}",
                        ["ID", "CPF"],
                        listar_reservas_por_quarto(cursor, numero),
                    )
    except psycopg2.Error as erro:
        print(f"Erro ao consultar o banco de dados: {erro}")


if __name__ == "__main__":
    main()
