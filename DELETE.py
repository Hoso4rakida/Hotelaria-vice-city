import psycopg2

def excluir_reserva(cursor, conexao, id_reserva):
    cursor.execute("DELETE FROM Reservas WHERE id_reserva = %s;", (id_reserva,))
    conexao.commit()
    return 0

def excluir_cliente(cursor, conexao, cpf):
    cursor.execute("DELETE FROM Hospedes WHERE cpf = %s;", (cpf,))
    conexao.commit()
    return 0
