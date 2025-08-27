#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
biblioteca.py

Sistema de Gerenciamento de Biblioteca
Implementação em Python utilizando Princípios de Programação Orientada a Objetos (POO).

Autor: [Seu Nome]
Data: YYYY-MM-DD
Versão: 1.0

Este módulo contém as classes e a interface de console para:
- Cadastro de livros
- Cadastro de usuários
- Empréstimo e devolução de livros
- Consulta de livros
- Geração de relatórios
"""

from datetime import date
from typing import Dict, List, Tuple

# -----------------------------------------------------------
# Definição de Exceções Customizadas
# -----------------------------------------------------------
class DuplicidadeLivroError(Exception):
    """Exceção lançada quando se tenta cadastrar um livro com ISBN já existente."""
    pass

class DuplicidadeUsuarioError(Exception):
    """Exceção lançada quando se tenta cadastrar um usuário com ID já existente."""
    pass

class LivroNaoEncontradoError(Exception):
    """Exceção lançada quando um livro não é encontrado no catálogo."""
    pass

class UsuarioNaoEncontradoError(Exception):
    """Exceção lançada quando um usuário não é encontrado no cadastro."""
    pass

class LivroIndisponivelError(Exception):
    """Exceção lançada quando não há cópias disponíveis para empréstimo."""
    pass

class EmprestimoDuplicadoError(Exception):
    """Exceção lançada quando o usuário já possui um empréstimo do mesmo livro."""
    pass

class DevolucaoInvalidaError(Exception):
    """Exceção lançada quando o usuário tenta devolver um livro que não possui emprestado."""
    pass

class ExcecaoDevolucaoInvalida(Exception):
    """Exceção lançada quando ocorre tentativa de devolver cópia além do total disponível."""
    pass


# -----------------------------------------------------------
# Classe Livro
# -----------------------------------------------------------
class Livro:
    """
    Representa um livro no acervo da biblioteca.

    Atributos:
        titulo (str): título da obra
        autor (str): autor da obra
        ano (int): ano de publicação
        isbn (str): código identificador único do livro
        total_copias (int): número total de cópias existentes
        copias_disponiveis (int): número de cópias disponíveis para empréstimo
    """

    def __init__(self, titulo: str, autor: str, ano: int, isbn: str, total_copias: int):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.isbn = isbn
        self.total_copias = total_copias
        self.copias_disponiveis = total_copias

    def emprestar(self):
        """
        Decrementa o número de cópias disponíveis para empréstimo.
        Levanta LivroIndisponivelError se não houver exemplares disponíveis.
        """
        if self.copias_disponiveis <= 0:
            raise LivroIndisponivelError(f"O livro '{self.titulo}' não possui cópias disponíveis.")
        self.copias_disponiveis -= 1

    def devolver(self):
        """
        Incrementa o número de cópias disponíveis.
        Levanta ExcecaoDevolucaoInvalida se o número de cópias disponíveis for igual ao total de cópias.
        """
        if self.copias_disponiveis >= self.total_copias:
            raise ExcecaoDevolucaoInvalida(f"Tentativa de devolver '{self.titulo}', mas todas as cópias já estão disponíveis.")
        self.copias_disponiveis += 1

    def __str__(self) -> str:
        """
        Representação textual do livro, exibindo título, autor, ano, ISBN e disponibilidade.
        """
        return (f"'{self.titulo}' | Autor: {self.autor} | Ano: {self.ano} | "
                f"ISBN: {self.isbn} | Disponíveis: {self.copias_disponiveis}/{self.total_copias}")


# -----------------------------------------------------------
# Classe Usuario
# -----------------------------------------------------------
class Usuario:
    """
    Representa um usuário cadastrado na biblioteca.

    Atributos:
        nome (str): nome completo do usuário
        id_usuario (str): identificador único do usuário
        contato (str): informação de contato (telefone ou e-mail)
        emprestimos_ativos (Dict[str, date]): dicionário com ISBN do livro como chave
                                              e data do empréstimo como valor
    """

    def __init__(self, nome: str, id_usuario: str, contato: str):
        self.nome = nome
        self.id_usuario = id_usuario
        self.contato = contato
        self.emprestimos_ativos: Dict[str, date] = {}

    def registrar_emprestimo(self, isbn: str, data_emprestimo: date):
        """
        Registra o empréstimo ativo de um livro para este usuário.
        Levanta EmprestimoDuplicadoError se o usuário já tiver o livro emprestado.
        """
        if isbn in self.emprestimos_ativos:
            raise EmprestimoDuplicadoError(f"O usuário '{self.nome}' já possui o livro com ISBN {isbn}.")
        self.emprestimos_ativos[isbn] = data_emprestimo

    def registrar_devolucao(self, isbn: str):
        """
        Remove o registro de empréstimo ativo de um livro para este usuário.
        Levanta DevolucaoInvalidaError se o ISBN não constar nos empréstimos ativos.
        """
        if isbn not in self.emprestimos_ativos:
            raise DevolucaoInvalidaError(f"O usuário '{self.nome}' não possui o livro com ISBN {isbn} emprestado.")
        del self.emprestimos_ativos[isbn]

    def __str__(self) -> str:
        """
        Representação textual do usuário, exibindo ID, nome e contato.
        """
        return f"ID: {self.id_usuario} | Nome: {self.nome} | Contato: {self.contato}"


# -----------------------------------------------------------
# Classe Biblioteca
# -----------------------------------------------------------
class Biblioteca:
    """
    Gerencia o catálogo de livros e o cadastro de usuários, além das operações de
    empréstimo, devolução, consulta e geração de relatórios.

    Atributos:
        catalogo (Dict[str, Livro]): mapeamento de ISBN para objeto Livro
        usuarios (Dict[str, Usuario]): mapeamento de id_usuario para objeto Usuario
    """

    def __init__(self):
        self.catalogo: Dict[str, Livro] = {}
        self.usuarios: Dict[str, Usuario] = {}

    def cadastrar_livro(self, titulo: str, autor: str, ano: int, isbn: str, total_copias: int):
        """
        Cadastra um novo livro no catálogo.
        Levanta DuplicidadeLivroError se já existir um livro com o ISBN informado.
        """
        if isbn in self.catalogo:
            raise DuplicidadeLivroError(f"Já existe um livro cadastrado com ISBN {isbn}.")
        novo_livro = Livro(titulo, autor, ano, isbn, total_copias)
        self.catalogo[isbn] = novo_livro

    def cadastrar_usuario(self, nome: str, id_usuario: str, contato: str):
        """
        Cadastra um novo usuário.
        Levanta DuplicidadeUsuarioError se já existir um usuário com o ID informado.
        """
        if id_usuario in self.usuarios:
            raise DuplicidadeUsuarioError(f"Já existe um usuário cadastrado com ID {id_usuario}.")
        novo_usuario = Usuario(nome, id_usuario, contato)
        self.usuarios[id_usuario] = novo_usuario

    def emprestar_livro(self, id_usuario: str, isbn: str):
        """
        Realiza o empréstimo de um livro para um usuário.
        Verifica existência de usuário e livro, disponibilidade e registra o empréstimo.
        """
        if id_usuario not in self.usuarios:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {id_usuario} não encontrado.")
        if isbn not in self.catalogo:
            raise LivroNaoEncontradoError(f"Livro com ISBN {isbn} não encontrado no catálogo.")

        usuario = self.usuarios[id_usuario]
        livro = self.catalogo[isbn]

        # Tenta efetuar o empréstimo no objeto Livro
        livro.emprestar()

        # Registra o empréstimo ativo no objeto Usuario
        data_hoje = date.today()
        usuario.registrar_emprestimo(isbn, data_hoje)

    def devolver_livro(self, id_usuario: str, isbn: str):
        """
        Realiza a devolução de um livro por um usuário.
        Verifica existência de usuário e livro, existência do empréstimo e atualiza cópias.
        """
        if id_usuario not in self.usuarios:
            raise UsuarioNaoEncontradoError(f"Usuário com ID {id_usuario} não encontrado.")
        if isbn not in self.catalogo:
            raise LivroNaoEncontradoError(f"Livro com ISBN {isbn} não encontrado no catálogo.")

        usuario = self.usuarios[id_usuario]
        livro = self.catalogo[isbn]

        # Remove o registro de empréstimo ativo do usuário
        usuario.registrar_devolucao(isbn)

        # Atualiza as cópias disponíveis do livro
        livro.devolver()

    def buscar_livros(self, campo: str, valor_busca: str) -> List[Livro]:
        """
        Busca livros conforme o campo informado (titulo, autor ou ano).
        Retorna lista de objetos Livro que correspondem ao critério de busca.
        """
        resultados: List[Livro] = []
        for livro in self.catalogo.values():
            if campo == 'titulo' and valor_busca.lower() in livro.titulo.lower():
                resultados.append(livro)
            elif campo == 'autor' and valor_busca.lower() in livro.autor.lower():
                resultados.append(livro)
            elif campo == 'ano':
                try:
                    ano_int = int(valor_busca)
                    if livro.ano == ano_int:
                        resultados.append(livro)
                except ValueError:
                    # Se não for um ano válido, ignora
                    pass
        return resultados

    def gerar_relatorio_livros_disponiveis(self) -> List[Livro]:
        """
        Retorna lista de livros com cópias disponíveis para empréstimo.
        """
        return [livro for livro in self.catalogo.values() if livro.copias_disponiveis > 0]

    def gerar_relatorio_livros_emprestados(self) -> List[Livro]:
        """
        Retorna lista de livros que estão com alguma cópia emprestada.
        """
        return [livro for livro in self.catalogo.values() if livro.copias_disponiveis < livro.total_copias]

    def gerar_relatorio_usuarios(self) -> List[Usuario]:
        """
        Retorna lista de todos os usuários cadastrados.
        """
        return list(self.usuarios.values())

    def gerar_relatorio_emprestimos_ativos(self) -> List[Tuple[Usuario, Livro, date]]:
        """
        Retorna lista de tuplas (Usuario, Livro, data_emprestimo) para cada empréstimo ativo.
        """
        relatorio = []
        for usuario in self.usuarios.values():
            for isbn, data_emprestimo in usuario.emprestimos_ativos.items():
                livro = self.catalogo.get(isbn)
                if livro:
                    relatorio.append((usuario, livro, data_emprestimo))
        return relatorio


# -----------------------------------------------------------
# Funções Auxiliares de Interface de Console
# -----------------------------------------------------------

def exibir_menu_principal():
    """
    Exibe o menu de opções principal do sistema.
    """
    print("\n========== SISTEMA DE GERENCIAMENTO DE BIBLIOTECA ==========")
    print("1. Cadastrar Livro")
    print("2. Cadastrar Usuário")
    print("3. Empréstimo de Livro")
    print("4. Devolução de Livro")
    print("5. Consulta de Livros")
    print("6. Relatórios")
    print("0. Sair")
    print("============================================================")


def cadastrar_livro_interface(bib: Biblioteca):
    """
    Interface para cadastrar um livro via entrada do usuário no console.
    """
    print("\n--- Cadastrar Livro ---")
    try:
        titulo = input("Título: ").strip()
        autor = input("Autor: ").strip()
        ano = int(input("Ano de publicação: ").strip())
        isbn = input("ISBN: ").strip()
        total_copias = int(input("Total de cópias: ").strip())
        bib.cadastrar_livro(titulo, autor, ano, isbn, total_copias)
        print("Livro cadastrado com sucesso!")
    except ValueError:
        print("Erro: 'Ano de publicação' e 'Total de cópias' devem ser números inteiros.")
    except DuplicidadeLivroError as e:
        print(f"Erro ao cadastrar livro: {e}")


def cadastrar_usuario_interface(bib: Biblioteca):
    """
    Interface para cadastrar um usuário via entrada do usuário no console.
    """
    print("\n--- Cadastrar Usuário ---")
    try:
        nome = input("Nome completo: ").strip()
        id_usuario = input("ID do usuário: ").strip()
        contato = input("Contato (telefone ou e-mail): ").strip()
        bib.cadastrar_usuario(nome, id_usuario, contato)
        print("Usuário cadastrado com sucesso!")
    except DuplicidadeUsuarioError as e:
        print(f"Erro ao cadastrar usuário: {e}")


def emprestar_livro_interface(bib: Biblioteca):
    """
    Interface para realizar empréstimo de livro via console.
    """
    print("\n--- Empréstimo de Livro ---")
    try:
        id_usuario = input("ID do usuário: ").strip()
        isbn = input("ISBN do livro: ").strip()
        bib.emprestar_livro(id_usuario, isbn)
        print("Empréstimo realizado com sucesso!")
    except (UsuarioNaoEncontradoError, LivroNaoEncontradoError,
            LivroIndisponivelError, EmprestimoDuplicadoError) as e:
        print(f"Erro ao emprestar livro: {e}")


def devolver_livro_interface(bib: Biblioteca):
    """
    Interface para realizar devolução de livro via console.
    """
    print("\n--- Devolução de Livro ---")
    try:
        id_usuario = input("ID do usuário: ").strip()
        isbn = input("ISBN do livro: ").strip()
        bib.devolver_livro(id_usuario, isbn)
        print("Devolução realizada com sucesso!")
    except (UsuarioNaoEncontradoError, LivroNaoEncontradoError,
            DevolucaoInvalidaError, ExcecaoDevolucaoInvalida) as e:
        print(f"Erro ao devolver livro: {e}")


def consulta_livros_interface(bib: Biblioteca):
    """
    Interface para consulta de livros por título, autor ou ano.
    """
    print("\n--- Consulta de Livros ---")
    print("Opções de busca:")
    print("1. Por título")
    print("2. Por autor")
    print("3. Por ano de publicação")
    escolha = input("Selecione (1-3): ").strip()

    if escolha == '1':
        campo = 'titulo'
        termo = input("Digite parte ou o título completo: ").strip()
    elif escolha == '2':
        campo = 'autor'
        termo = input("Digite parte ou o nome completo do autor: ").strip()
    elif escolha == '3':
        campo = 'ano'
        termo = input("Digite o ano de publicação: ").strip()
    else:
        print("Opção de busca inválida.")
        return

    resultados = bib.buscar_livros(campo, termo)
    if resultados:
        print(f"\nForam encontrados {len(resultados)} resultado(s):")
        for livro in resultados:
            print(f"- {livro}")
    else:
        print("Nenhum livro encontrado para o critério informado.")


def relatorios_interface(bib: Biblioteca):
    """
    Interface para geração de relatórios diversos.
    """
    while True:
        print("\n--- Relatórios ---")
        print("1. Livros disponíveis")
        print("2. Livros emprestados")
        print("3. Usuários cadastrados")
        print("4. Empréstimos ativos")
        print("0. Voltar ao menu principal")
        escolha = input("Selecione (0-4): ").strip()

        if escolha == '1':
            disponiveis = bib.gerar_relatorio_livros_disponiveis()
            print(f"\nTotal de livros disponíveis: {len(disponiveis)}")
            for livro in disponiveis:
                print(f"- {livro}")
        elif escolha == '2':
            emprestados = bib.gerar_relatorio_livros_emprestados()
            print(f"\nTotal de livros com cópias emprestadas: {len(emprestados)}")
            for livro in emprestados:
                copias_emprestadas = livro.total_copias - livro.copias_disponiveis
                print(f"- {livro} | Emprestadas: {copias_emprestadas}")
        elif escolha == '3':
            usuarios = bib.gerar_relatorio_usuarios()
            print(f"\nTotal de usuários cadastrados: {len(usuarios)}")
            for usuario in usuarios:
                print(f"- {usuario}")
        elif escolha == '4':
            emprestimos_ativos = bib.gerar_relatorio_emprestimos_ativos()
            print(f"\nTotal de empréstimos ativos: {len(emprestimos_ativos)}")
            for usuario, livro, data_emp in emprestimos_ativos:
                print(f"- Usuário: {usuario.nome} (ID: {usuario.id_usuario}) | "
                      f"Livro: '{livro.titulo}' (ISBN: {livro.isbn}) | Data do Empréstimo: {data_emp}")
        elif escolha == '0':
            break
        else:
            print("Opção inválida. Tente novamente.")


# -----------------------------------------------------------
# Função Principal
# -----------------------------------------------------------
def main():
    """
    Ponto de entrada da aplicação. Exibe o menu principal e redireciona para as funcionalidades.
    """
    biblioteca = Biblioteca()

    while True:
        exibir_menu_principal()
        opcao = input("Selecione uma opção (0-6): ").strip()

        if opcao == '1':
            cadastrar_livro_interface(biblioteca)
        elif opcao == '2':
            cadastrar_usuario_interface(biblioteca)
        elif opcao == '3':
            emprestar_livro_interface(biblioteca)
        elif opcao == '4':
            devolver_livro_interface(biblioteca)
        elif opcao == '5':
            consulta_livros_interface(biblioteca)
        elif opcao == '6':
            relatorios_interface(biblioteca)
        elif opcao == '0':
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, selecione uma opção válida (0-6).")


if __name__ == '__main__':
    main()
