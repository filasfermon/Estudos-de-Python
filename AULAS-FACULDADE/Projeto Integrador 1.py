# Classe Livro
class Livro:
    def __init__(self, titulo, autor, ano, copias):
        self.titulo = titulo
        self.autor = autor
        self.ano = ano
        self.copias = copias

    def __str__(self):
        return f"{self.titulo} ({self.ano}) - {self.autor} - Cópias: {self.copias}"

# Classe Usuario
class Usuario:
    def __init__(self, nome, id_usuario, contato):
        self.nome = nome
        self.id_usuario = id_usuario
        self.contato = contato
        self.livros_emprestados = []

    def __str__(self):
        return f"{self.nome} (ID: {self.id_usuario})"

# Classe Biblioteca
class Biblioteca:
    def __init__(self):
        self.livros = []
        self.usuarios = []

    def cadastrar_livro(self, livro):
        self.livros.append(livro)

    def cadastrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def encontrar_livro(self, titulo):
        for livro in self.livros:
            if livro.titulo.lower() == titulo.lower():
                return livro
        return None

    def emprestar_livro(self, id_usuario, titulo):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        livro = self.encontrar_livro(titulo)
        if usuario and livro:
            if livro.copias > 0:
                livro.copias -= 1
                usuario.livros_emprestados.append(livro.titulo)
                print(f"{livro.titulo} emprestado com sucesso para {usuario.nome}.")
            else:
                print("Livro indisponível para empréstimo.")
        else:
            print("Usuário ou livro não encontrado.")

    def devolver_livro(self, id_usuario, titulo):
        usuario = next((u for u in self.usuarios if u.id_usuario == id_usuario), None)
        livro = self.encontrar_livro(titulo)
        if usuario and livro and titulo in usuario.livros_emprestados:
            livro.copias += 1
            usuario.livros_emprestados.remove(titulo)
            print(f"{titulo} devolvido com sucesso.")
        else:
            print("Erro na devolução. Verifique os dados.")

    def consultar_livros(self, filtro=None):
        for livro in self.livros:
            if not filtro or filtro.lower() in livro.titulo.lower() or filtro.lower() in livro.autor.lower():
                print(livro)

    def relatorios(self):
        print("\n📚 Livros Disponíveis:")
        for livro in self.livros:
            print(livro)
        print("\n👤 Usuários Cadastrados:")
        for usuario in self.usuarios:
            print(usuario)

# Interface de menu
def menu():
    biblio = Biblioteca()

    while True:
        print("\n--- MENU ---")
        print("1. Cadastrar Livro")
        print("2. Cadastrar Usuário")
        print("3. Empréstimo de Livro")
        print("4. Devolução de Livro")
        print("5. Consultar Livros")
        print("6. Relatórios")
        print("7. Sair")

        opcao = input("Escolha uma opção: ")

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

menu()
