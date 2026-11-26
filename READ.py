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
                imprimir_registros(
                    "Hospedes", ["CPF", "Nome", "E-mail", "Telefone"],
                    listar_hospedes(cursor),
                )
                imprimir_registros(
                    "Quartos", ["Numero", "Tipo", "Capacidade", "Preco da diaria"],
                    listar_quartos(cursor),
                )
                imprimir_registros(
                    "Reservas", ["ID", "CPF", "Hospede", "Quarto", "Tipo", "Preco"],
                    listar_reservas(cursor),
                )
    except psycopg2.Error as erro:
        print(f"Erro ao consultar o banco: {erro}")


if __name__ == "__main__":
    main()
