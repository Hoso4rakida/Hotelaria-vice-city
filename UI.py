import os
from contextlib import closing

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
                            cpf = input(f"{AZUL}CPF do cliente (000.000.000-00): {RESET}").strip()
                            nome = input(f"{AZUL}Novo nome: {RESET}").strip()
                            email = input(f"{AZUL}Novo e-mail: {RESET}").strip()
                            telefone = input(f"{AZUL}Novo telefone: {RESET}").strip()
                            UPDATE.atualizar(cursor, conexao, cpf, nome, email, telefone)
                        elif opcao == "5":
                            READ.consultar(cursor)
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
