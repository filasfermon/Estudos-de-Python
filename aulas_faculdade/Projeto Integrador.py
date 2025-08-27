# Classe Livro representa uma obra com título, autor, ano e número de cópias disponíveis
class Livro:
    def __init__(self, titulo, autor, ano, copias):
        self.titulo = titulo      # Título do livro
        self.autor = autor        # Autor do livro
        self.ano = ano            # Ano de publicação
        self.copias = copias      # Quantidade de cópias disponíveis

    def __str__(self):
        # Representação textual do objeto Livro, útil para exibição em tela
        return f"{self.titulo} ({self.ano}) - {self.autor} - Cópias: {self.copias}"


# Classe Usuario representa um usuário da biblioteca com identificação e livros emprestados
class Usuario:
    def __init__(self, nome, id_usuario, contato):
        self.nome = nome                      # Nome do usuário
        self.id_usuario = id_usuario          # Identificador único do usuário
        self.contato = contato                # Informações de contato
        self.livros_emprestados = []          # Lista de títulos de livros emprestados

    def __str__(self):
        # Representação textual do objeto Usuario
        return f"{self.nome} (ID: {self.id_usuario})"


# Classe Biblioteca gerencia os livros e usuários, além das operações principais
class Biblioteca:
    def __init__(self):
        self.livros = []       # Lista de objetos do tipo Livro cadastrados
        self.usuarios = []     # Lista de objetos do tipo Usuario cadastrados

    def cadastrar_livro(self, livro):
        # Adiciona um novo livro à lista de livros da biblioteca
        self.livros.append(livro)

    def cadastrar_usuario(self, usuario):
        # Adiciona um novo usuário à lista de usuários da biblioteca
        self.usuarios.append(usuario)

    def encontrar_livro(self, titulo):
        # Procura um livro pelo título (ignorando maiúsculas/minúsculas)
        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():
                return livro
        return None  # Retorna None se o livro não for encontrado

    def emprestar_livro(self, id_usuario, titulo):
        # Realiza o empréstimo de um livro para um usuário específico
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        livro = self.encontrar_livro(titulo)
        if usuario and livro:
            if livro.copias > 0:
                livro.copias -= 1                         # Diminui a quantidade de cópias
                usuario.livros_emprestados.append(livro.titulo)  # Registra o empréstimo
                print(f"{livro.titulo} emprestado com sucesso para {usuario.nome}.")
            else:
                print("Livro indisponível para empréstimo.")
        else:
            print("Usuário ou livro não encontrado.")

    def devolver_livro(self, id_usuario, titulo):
        # Realiza a devolução de um livro por parte de um usuário
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        livro = self.encontrar_livro(titulo)
        if usuario and livro and titulo in usuario.livros_emprestados:
            livro.copias += 1                            # Aumenta a quantidade de cópias disponíveis
            usuario.livros_emprestados.remove(titulo)    # Remove o título da lista de empréstimos
            print(f"{titulo} devolvido com sucesso.")
        else:
            print("Erro na devolução. Verifique os dados.")

    def consultar_livros(self, filtro=None):
        # Exibe os livros cadastrados, podendo filtrar por título ou autor
        for livro in self.livros:
            if not filtro or filtro.lower() in livro.titulo.lower() or filtro.lower() in livro.autor.lower():
                print(livro)

    def relatorios(self):
        # Exibe todos os livros e usuários cadastrados no sistema
        print("\n📚 Livros Disponíveis:")
        for livro in self.livros:
            print(livro)
        print("\n👤 Usuários Cadastrados:")
        for usuario in self.usuarios:
            print(usuario)


# Função de menu principal do programa
def menu():
    biblio = Biblioteca()  # Instancia a biblioteca

    while True:
        # Menu interativo apresentado ao usuário
        print("\n--- MENU ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Empréstimo de Livro")
        print("4. Devolução de Livro")
        print("5. Consultar Livros")
        print("6. Relatórios")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

        # Tratamento das opções do menu
        if opcao == '1':
            t = input("Título: ")
            a = input("Autor: ")
            an = input("Ano: ")
            c = int(input("Cópias: "))
            biblio.cadastrar_livro(Livro(t, a, an, c))

        elif opcao == '2':
            n = input("Nome: ")
            i = input("ID: ")
            ct = input("Contato: ")
            biblio.cadastrar_usuario(Usuario(n, i, ct))

        elif opcao == '3':
            uid = input("ID do usuário: ")
            titulo = input("Título do livro: ")
            biblio.emprestar_livro(uid, titulo)

        elif opcao == '4':
            uid = input("ID do usuário: ")
            titulo = input("Título do livro: ")
            biblio.devolver_livro(uid, titulo)

        elif opcao == '5':
            f = input("Filtro (título/autor): ")
            biblio.consultar_livros(f)

        elif opcao == '6':
            biblio.relatorios()

        elif opcao == '7':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


# Execução do programa
menu()
