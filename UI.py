import os
import re
from contextlib import closing
from decimal import Decimal, InvalidOperation

import psycopg2

import CREATE
import DELETE
import READ
import UPDATE

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


def normalizar_cpf(cpf):
    """Remove a mascara do CPF para comparar com o valor gravado no banco."""
    return re.sub(r"\D", "", cpf)


def ler_texto_opcional(mensagem):
    """Enter mantém o valor atual do campo."""
    return input(mensagem).strip() or None


def ler_inteiro_opcional(mensagem):
    """Enter mantém o valor atual; caso contrário, lê um inteiro positivo."""
    while True:
        valor = input(mensagem).strip()
        if not valor:
            return None
        if valor.isdigit():
            return int(valor)
        print(f"{VERMELHO}Digite apenas numeros.{RESET}")


def ler_preco_opcional(mensagem):
    """Enter mantém o valor atual; caso contrário, lê um preço decimal."""
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        if not valor:
            return None
        try:
            return Decimal(valor)
        except InvalidOperation:
            print(f"{VERMELHO}Digite um preco valido.{RESET}")


def cadastrar_cliente(cursor, conexao):
    cpf = input(f"{AZUL}CPF (000.000.000-00): {RESET}").strip()
    nome = input(f"{AZUL}Nome: {RESET}").strip()
    email = input(f"{AZUL}E-mail: {RESET}").strip()
    telefone = input(f"{AZUL}Telefone: {RESET}").strip()
    try:
        CREATE.cadastrar_cliente(cursor, cpf, nome, email, telefone)
        conexao.commit()
        print(f"\n{VERDE}Cliente cadastrado!{RESET}")
    except psycopg2.Error as erro:
        conexao.rollback()
        print(f"\n{VERMELHO}Erro: {erro}{RESET}")


def atualizar_cliente(conexao):
    cpf = normalizar_cpf(
        input(f"{AZUL}CPF do cliente (000.000.000-00): {RESET}").strip()
    )
    nome = ler_texto_opcional(f"{AZUL}Novo nome (Enter para manter): {RESET}")
    email = ler_texto_opcional(f"{AZUL}Novo e-mail (Enter para manter): {RESET}")
    telefone = ler_texto_opcional(f"{AZUL}Novo telefone (Enter para manter): {RESET}")

    if UPDATE.atualizar_hospede(conexao, cpf, nome, email, telefone):
        print(f"\n{VERDE}Cliente atualizado!{RESET}")
    else:
        print(f"\n{AMARELO}Cliente nao encontrado.{RESET}")


def atualizar_quarto(conexao):
    numero = ler_inteiro(f"{AZUL}Numero do quarto: {RESET}")
    tipo = ler_texto_opcional(f"{AZUL}Novo tipo (Enter para manter): {RESET}")
    capacidade = ler_inteiro_opcional(
        f"{AZUL}Nova capacidade (Enter para manter): {RESET}"
    )
    preco_diaria = ler_preco_opcional(
        f"{AZUL}Novo preco da diaria (Enter para manter): {RESET}"
    )

    if UPDATE.atualizar_quarto(conexao, numero, tipo, capacidade, preco_diaria):
        print(f"\n{VERDE}Quarto atualizado!{RESET}")
    else:
        print(f"\n{AMARELO}Quarto nao encontrado.{RESET}")


def main():
    try:
        with closing(READ.conectar()) as conexao:
            with conexao.cursor() as cursor:
                while True:
                    cabecalho()
                    print(f"\n  {NEGRITO}[1]{RESET} Cadastrar cliente")
                    print(f"  {NEGRITO}[2]{RESET} Excluir reserva")
                    print(f"  {NEGRITO}[3]{RESET} Excluir cliente (e suas reservas)")
                    print(f"  {NEGRITO}[4]{RESET} Atualizar cliente")
                    print(f"  {NEGRITO}[5]{RESET} Consultar dados")
                    print(f"  {NEGRITO}[6]{RESET} Atualizar quarto")
                    print(f"  {NEGRITO}[0]{RESET} Sair")
                    opcao = input(f"\n{AZUL}Escolha: {RESET}").strip()

                    try:
                        if opcao == "1":
                            cadastrar_cliente(cursor, conexao)
                        elif opcao == "2":
                            id_reserva = ler_inteiro(f"{AZUL}ID da reserva: {RESET}")
                            DELETE.excluir_reserva(cursor, conexao, id_reserva)
                        elif opcao == "3":
                            cpf = input(f"{AZUL}CPF do cliente (000.000.000-00): {RESET}").strip()
                            DELETE.excluir_cliente(cursor, conexao, cpf)
                        elif opcao == "4":
                            atualizar_cliente(conexao)
                        elif opcao == "5":
                            READ.consultar(cursor)
                        elif opcao == "6":
                            atualizar_quarto(conexao)
                        elif opcao == "0":
                            print(f"\n{VERDE}Ate logo!{RESET}\n")
                            break
                        else:
                            print(f"\n{VERMELHO}Opcao invalida.{RESET}")
                    except Exception as erro:
                        print(f"\n{VERMELHO}Erro: {erro}{RESET}")
                    esperar()
    except psycopg2.Error as erro:
        print(f"{VERMELHO}Erro no banco: {erro}{RESET}")


if __name__ == "__main__":
    main()
