import os
from contextlib import closing

import psycopg2

import DELETE
import UPDATE
from READ import (
    conectar,
    imprimir_registros,
    listar_hospedes,
    listar_quartos,
    listar_reservas,
)

AZUL = "\033[94m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
VERMELHO = "\033[91m"
NEGRITO = "\033[1m"
RESET = "\033[0m"


def cabecalho():
    os.system("cls" if os.name == "nt" else "clear")
    titulo = "  HOTELARIA VICE CITY  -  MENU PRINCIPAL"
    print(f"{AZUL}╔{'═' * 52}╗{RESET}")
    print(f"{AZUL}║{RESET}{NEGRITO}{titulo:<52}{RESET}{AZUL}║{RESET}")
    print(f"{AZUL}╚{'═' * 52}╝{RESET}")


def esperar():
    input(f"\n{AMARELO}Tecle Enter para continuar...{RESET}")


def ler_inteiro(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor.isdigit():
            return int(valor)
        print(f"{VERMELHO}Digite apenas numeros.{RESET}")


def cadastrar_cliente(cursor, conexao):
    cpf = ler_inteiro(f"{AZUL}CPF: {RESET}")
    nome = input(f"{AZUL}Nome: {RESET}").strip()
    email = input(f"{AZUL}E-mail: {RESET}").strip()
    telefone = input(f"{AZUL}Telefone: {RESET}").strip()
    try:
        cursor.execute(
            "INSERT INTO Hospedes (cpf, nome, email, telefone) VALUES (%s, %s, %s, %s);",
            (cpf, nome, email, telefone),
        )
        conexao.commit()
        print(f"\n{VERDE}Cliente cadastrado!{RESET}")
    except psycopg2.Error as erro:
        conexao.rollback()
        print(f"\n{VERMELHO}Erro: {erro}{RESET}")


def excluir_reserva(cursor, conexao):
    id_reserva = ler_inteiro(f"{AZUL}ID da reserva: {RESET}")
    try:
        apagadas = DELETE.deletar_reserva(cursor, id_reserva)
        conexao.commit()
        if apagadas:
            print(f"\n{VERDE}Reserva excluida!{RESET}")
        else:
            print(f"\n{AMARELO}Reserva nao encontrada.{RESET}")
    except psycopg2.Error as erro:
        conexao.rollback()
        print(f"\n{VERMELHO}Erro: {erro}{RESET}")


def excluir_cliente(cursor, conexao):
    cpf = ler_inteiro(f"{AZUL}CPF do cliente: {RESET}")
    try:
        apagadas = DELETE.deletar_hospede(cursor, cpf)
        conexao.commit()
        if apagadas:
            print(f"\n{VERDE}Cliente excluido!{RESET}")
        else:
            print(f"\n{AMARELO}Cliente nao encontrado.{RESET}")
    except psycopg2.Error as erro:
        conexao.rollback()
        print(f"\n{VERMELHO}Erro: {erro}{RESET}")


def atualizar_cliente(cursor, conexao):
    cpf = ler_inteiro(f"{AZUL}CPF do cliente: {RESET}")
    nome = input(f"{AZUL}Novo nome: {RESET}").strip()
    email = input(f"{AZUL}Novo e-mail: {RESET}").strip()
    telefone = input(f"{AZUL}Novo telefone: {RESET}").strip()
    try:
        alteradas = UPDATE.atualizar_cliente(cursor, cpf, nome, email, telefone)
        conexao.commit()
        if alteradas:
            print(f"\n{VERDE}Cliente atualizado!{RESET}")
        else:
            print(f"\n{AMARELO}Cliente nao encontrado.{RESET}")
    except psycopg2.Error as erro:
        conexao.rollback()
        print(f"\n{VERMELHO}Erro: {erro}{RESET}")


def consultar(cursor):
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


def main():
    try:
        with closing(conectar()) as conexao:
            with conexao.cursor() as cursor:
                while True:
                    cabecalho()
                    print(f"\n  {NEGRITO}[1]{RESET} Cadastrar cliente")
                    print(f"  {NEGRITO}[2]{RESET} Excluir reserva")
                    print(f"  {NEGRITO}[3]{RESET} Excluir cliente (e suas reservas)")
                    print(f"  {NEGRITO}[4]{RESET} Atualizar cliente")
                    print(f"  {NEGRITO}[5]{RESET} Consultar dados")
                    print(f"  {NEGRITO}[0]{RESET} Sair")
                    opcao = input(f"\n{AZUL}Escolha: {RESET}").strip()

                    if opcao == "1":
                        cadastrar_cliente(cursor, conexao)
                    elif opcao == "2":
                        excluir_reserva(cursor, conexao)
                    elif opcao == "3":
                        excluir_cliente(cursor, conexao)
                    elif opcao == "4":
                        atualizar_cliente(cursor, conexao)
                    elif opcao == "5":
                        consultar(cursor)
                    elif opcao == "0":
                        print(f"\n{VERDE}Ate logo!{RESET}\n")
                        break
                    else:
                        print(f"\n{VERMELHO}Opcao invalida.{RESET}")
                    esperar()
    except psycopg2.Error as erro:
        print(f"{VERMELHO}Erro no banco: {erro}{RESET}")


if __name__ == "__main__":
    main()
