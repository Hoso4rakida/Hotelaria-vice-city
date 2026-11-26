from decimal import Decimal, InvalidOperation

from psycopg2.extensions import connection as Connection

import re


def validar_cpf(cpf: str) -> None:
    """Verifica se o CPF possui exatamente 11 dígitos numéricos."""

    if not isinstance(cpf, str):
        raise TypeError("O CPF deve ser uma string.")

    if not re.fullmatch(r"\d{11}", cpf):
        raise ValueError("O CPF deve conter exatamente 11 dígitos.")


def validar_texto(valor: str, campo: str, limite: int) -> None:
    """Valida o tipo, o conteúdo e o limite de caracteres de um texto."""

    if not isinstance(valor, str):
        raise TypeError(f"{campo} deve ser uma string.")

    if not valor.strip():
        raise ValueError(f"{campo} não pode ser vazio.")

    if len(valor) > limite:
        raise ValueError(f"{campo} não pode ultrapassar {limite} caracteres.")


def validar_email(email: str) -> None:
    """Valida a estrutura básica de um endereço de e-mail."""

    validar_texto(email, "E-mail", 100)

    padrao = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(padrao, email):
        raise ValueError("Formato de e-mail inválido.")


def validar_telefone(telefone: str) -> None:
    """Verifica se o telefone possui entre 10 e 13 dígitos."""

    validar_texto(telefone, "Telefone", 15)

    digitos = re.sub(r"\D", "", telefone)

    if not 10 <= len(digitos) <= 13:
        raise ValueError("Telefone deve conter entre 10 e 13 dígitos.")


def validar_inteiro_positivo(valor: int, campo: str) -> None:
    """Verifica se o valor é um número inteiro positivo."""

    if isinstance(valor, bool) or not isinstance(valor, int):
        raise TypeError(f"{campo} deve ser um número inteiro.")

    if valor <= 0:
        raise ValueError(f"{campo} deve ser maior que zero.")


def validar_preco(preco: Decimal) -> None:
    """Valida se o preço é positivo, finito e possui no máximo duas casas decimais efetivas."""

    if not isinstance(preco, Decimal):
        raise TypeError("O preço deve ser um Decimal.")

    if not preco.is_finite():
        raise ValueError("O preço deve ser finito.")

    if preco <= 0:
        raise ValueError("O preço deve ser maior que zero.")

    try:
        preco_arredondado = preco.quantize(Decimal("0.01"))
    except InvalidOperation as erro:
        raise ValueError(
            "O preço não pode ser representado com duas casas decimais."
        ) from erro

    if preco != preco_arredondado:
        raise ValueError("O preço deve possuir no máximo duas casas decimais.")


def atualizar_hospede(
    conexao: Connection,
    cpf: str,
    nome: str | None = None,
    email: str | None = None,
    telefone: str | None = None
) -> bool:
    """
    Atualiza os dados de um hóspede identificado pelo CPF.

    Os campos que receberem None permanecerão inalterados.

    Retorna True se o registro existir.
    Retorna False se nenhum registro corresponder ao CPF.
    """

    validar_cpf(cpf)

    if nome is None and email is None and telefone is None:
        raise ValueError("Informe pelo menos um campo para atualizar.")

    if nome is not None:
        validar_texto(nome, "Nome", 100)

    if email is not None:
        validar_email(email)

    if telefone is not None:
        validar_telefone(telefone)

    try:
        with conexao.cursor() as cursor:

            cursor.execute("""
                UPDATE Hospedes
                SET Nome = COALESCE(%s, Nome),
                    email = COALESCE(%s, email),
                    telefone = COALESCE(%s, telefone)
                WHERE cpf = %s;
            """, (nome, email, telefone, cpf))

            atualizado = cursor.rowcount > 0

        conexao.commit()
        return atualizado

    except Exception:
        conexao.rollback()
        raise


def atualizar_quarto(
    conexao: Connection,
    numero: int,
    tipo: str | None = None,
    capacidade: int | None = None,
    preco_diaria: Decimal | None = None
) -> bool:
    """
    Atualiza as informações de um quarto identificado pelo número.

    Os campos que receberem None permanecerão inalterados.

    Retorna True se o registro existir.
    Retorna False se nenhum registro corresponder ao número.
    """

    validar_inteiro_positivo(numero, "Número do quarto")

    if tipo is None and capacidade is None and preco_diaria is None:
        raise ValueError("Informe pelo menos um campo para atualizar.")

    if tipo is not None:
        validar_texto(tipo, "Tipo", 50)

    if capacidade is not None:
        validar_inteiro_positivo(capacidade, "Capacidade")

    if preco_diaria is not None:
        validar_preco(preco_diaria)

    try:
        with conexao.cursor() as cursor:

            cursor.execute("""
                UPDATE Quartos
                SET tipo = COALESCE(%s, tipo),
                    capacidade = COALESCE(%s, capacidade),
                    preco_diaria = COALESCE(%s, preco_diaria)
                WHERE numero = %s;
            """, (tipo, capacidade, preco_diaria, numero))

            atualizado = cursor.rowcount > 0

        conexao.commit()
        return atualizado

    except Exception:
        conexao.rollback()
        raise


def atualizar_reserva(
    conexao: Connection,
    id_reserva: int,
    cpf_hospede: str | None = None,
    numero_quarto: int | None = None
) -> bool:
    """
    Atualiza o hóspede ou o quarto associado a uma reserva.

    Os campos que receberem None permanecerão inalterados.

    Retorna True se o registro existir.
    Retorna False se nenhum registro corresponder ao ID.
    """

    validar_inteiro_positivo(id_reserva, "ID da reserva")

    if cpf_hospede is None and numero_quarto is None:
        raise ValueError("Informe pelo menos um campo para atualizar.")

    if cpf_hospede is not None:
        validar_cpf(cpf_hospede)

    if numero_quarto is not None:
        validar_inteiro_positivo(numero_quarto, "Número do quarto")

    try:
        with conexao.cursor() as cursor:

            cursor.execute("""
                UPDATE Reservas
                SET cpf_hospede = COALESCE(%s, cpf_hospede),
                    numero_quarto = COALESCE(%s, numero_quarto)
                WHERE id_reserva = %s;
            """, (cpf_hospede, numero_quarto, id_reserva))

            atualizado = cursor.rowcount > 0

        conexao.commit()
        return atualizado

    except Exception:
        conexao.rollback()
        raise