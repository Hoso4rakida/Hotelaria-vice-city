def cadastrar_cliente(cursor, cpf, nome, email, telefone):
    cursor.execute(
        "INSERT INTO Hospedes (cpf, nome, email, telefone) VALUES (%s, %s, %s, %s);",
        (cpf, nome, email, telefone),
    )
    return cursor.rowcount
