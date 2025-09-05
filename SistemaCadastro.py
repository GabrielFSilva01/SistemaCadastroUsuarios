import sqlite3
import tkinter as tk

# Inicializar a conexão com o banco de dados
def inicializar_banco():
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            telefone TEXT NOT NULL,
            CPF TEXT NOT NULL UNIQUE,
            data_cadastro TEXT DEFAULT (datetime('now','localtime'))
        )
    ''')
    conexao.commit()
    conexao.close()

# Função para cadastrar um novo usuário
def cadastrar_usuario(nome, email, telefone, CPF):
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO usuarios (nome, email, telefone, CPF)
            VALUES (?, ?, ?, ?)
        ''', (nome, email, telefone, CPF))
        conexao.commit()
        print("Usuário cadastrado com sucesso!")
    except sqlite3.IntegrityError:
        print("Erro: CPF já cadastrado.")
    finally:
        conexao.close()

# Função para listar todos os usuários
def listar_usuarios():
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conexao.close()
    if usuarios:
        for usuario in usuarios:
            print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Telefone: {usuario[3]}, CPF: {usuario[4]}, Data de Cadastro: {usuario[5]}")
            print("-" * 50)
    else:
        print("Nenhum usuário cadastrado.")

# Função para buscar um usuário pelo CPF
def buscar_usuario_por_CPF(CPF):
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE CPF = ?', (CPF,))
    usuario = cursor.fetchone()
    conexao.close()
    if usuario:
        print(f"ID: {usuario[0]}, Nome: {usuario[1]}, Email: {usuario[2]}, Telefone: {usuario[3]}, CPF: {usuario[4]}, Data de Cadastro: {usuario[5]}")
    else:
        print("Usuário não encontrado.")

# Função para atualizar os dados de um usuário pelo CPF
def atualizar_usuario(CPF, novo_nome=None, novo_email=None, novo_telefone=None):
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    cursor.execute('''
        UPDATE usuarios
        SET nome = ?, email = ?, telefone = ?
        WHERE CPF = ?
    ''', (novo_nome, novo_email, novo_telefone, CPF))
    conexao.commit()

    if cursor.rowcount == 0:
        print("Usuário não encontrado.")
    else:
        print("Usuário atualizado com sucesso!")
    conexao.close()

# Função para deletar um usuário
def deletar_usuario(CPF):
    conexao = sqlite3.connect('cadastro.db')
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM usuarios WHERE CPF = ?', (CPF,))
    conexao.commit()
    if cursor.rowcount == 0:
        print("Usuário não encontrado.")
    else:
        print("Usuário deletado com sucesso!")
    conexao.close()

# Interface gráfica com Tkinter
def interface_grafica():
    root = tk.Tk()
    root.title("Sistema de Cadastro")

    # --- Funções internas --- #
    def cadastrar():
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        CPF = entry_CPF.get()
        cadastrar_usuario(nome, email, telefone, CPF)
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)
        entry_CPF.delete(0, tk.END)

    def listar():
        listar_usuarios()

    def buscar():
        CPF = entry_CPF_buscar.get()
        buscar_usuario_por_CPF(CPF)
        entry_CPF_buscar.delete(0, tk.END)

    def atualizar():
        CPF = entry_CPF_atualizar.get()
        novo_nome = entry_novo_nome.get()
        novo_email = entry_novo_email.get()
        novo_telefone = entry_novo_telefone.get()
        atualizar_usuario(CPF, novo_nome, novo_email, novo_telefone)
        entry_CPF_atualizar.delete(0, tk.END)
        entry_novo_nome.delete(0, tk.END)
        entry_novo_email.delete(0, tk.END)
        entry_novo_telefone.delete(0, tk.END)

    def deletar():
        CPF = entry_CPF_deletar.get()
        deletar_usuario(CPF)
        entry_CPF_deletar.delete(0, tk.END)

    # --- Layout --- #

    # Frame de busca
    frame_buscar = tk.Frame(root)
    frame_buscar.pack(pady=10)
    tk.Label(frame_buscar, text="Buscar CPF:").grid(row=0, column=0)
    entry_CPF_buscar = tk.Entry(frame_buscar)
    entry_CPF_buscar.grid(row=0, column=1)
    tk.Button(frame_buscar, text="Buscar", command=buscar).grid(row=0, column=2, padx=5)

    # Frame de atualização
    frame_atualizar = tk.Frame(root)
    frame_atualizar.pack(pady=10)
    tk.Label(frame_atualizar, text="CPF para atualizar:").grid(row=0, column=0)
    entry_CPF_atualizar = tk.Entry(frame_atualizar)
    entry_CPF_atualizar.grid(row=0, column=1)
    tk.Label(frame_atualizar, text="Novo Nome:").grid(row=1, column=0)
    entry_novo_nome = tk.Entry(frame_atualizar)
    entry_novo_nome.grid(row=1, column=1)
    tk.Label(frame_atualizar, text="Novo Email:").grid(row=2, column=0)
    entry_novo_email = tk.Entry(frame_atualizar)
    entry_novo_email.grid(row=2, column=1)
    tk.Label(frame_atualizar, text="Novo Telefone:").grid(row=3, column=0)
    entry_novo_telefone = tk.Entry(frame_atualizar)
    entry_novo_telefone.grid(row=3, column=1)
    tk.Button(frame_atualizar, text="Atualizar", command=atualizar).grid(row=4, columnspan=2, pady=5)

    # Frame de deleção
    frame_deletar = tk.Frame(root)
    frame_deletar.pack(pady=10)
    tk.Label(frame_deletar, text="CPF para deletar:").grid(row=0, column=0)
    entry_CPF_deletar = tk.Entry(frame_deletar)
    entry_CPF_deletar.grid(row=0, column=1)
    tk.Button(frame_deletar, text="Deletar", command=deletar).grid(row=0, column=2, padx=5)

    # Frame de cadastro
    frame_cadastro = tk.Frame(root)
    frame_cadastro.pack(pady=10)
    tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(frame_cadastro)
    entry_nome.grid(row=0, column=1)
    tk.Label(frame_cadastro, text="Email:").grid(row=1, column=0)
    entry_email = tk.Entry(frame_cadastro)
    entry_email.grid(row=1, column=1)
    tk.Label(frame_cadastro, text="Telefone:").grid(row=2, column=0)
    entry_telefone = tk.Entry(frame_cadastro)
    entry_telefone.grid(row=2, column=1)
    tk.Label(frame_cadastro, text="CPF:").grid(row=3, column=0)
    entry_CPF = tk.Entry(frame_cadastro)
    entry_CPF.grid(row=3, column=1)
    tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar).grid(row=4, columnspan=2, pady=5)

    # Botão para listar usuários no console
    tk.Button(root, text="Listar Usuários", command=listar).pack(pady=5)

    root.mainloop()

# Inicializa o banco e abre a interface
if __name__ == "__main__":
    inicializar_banco()
    interface_grafica()
