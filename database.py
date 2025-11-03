import sqlite3

# Criar conexão com o banco de dados
conn = sqlite3.connect("estoque_produtos.db")
cursor = conn.cursor()

# Criar tabela de produtos
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sku TEXT UNIQUE NOT NULL,
    quantidade INTEGER NOT NULL
)
''')

# Criar tabela de movimentações
cursor.execute('''
CREATE TABLE IF NOT EXISTS movimentacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    tipo TEXT CHECK(tipo IN ('entrada', 'saida')) NOT NULL,
    quantidade INTEGER NOT NULL,
    data TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')

# res = cursor.execute("DELETE FROM movimentacoes")
# res2 = cursor.execute("DELETE FROM movimentacoes")
# print(res.fetchall())
# print(res2.fetchall())

conn.commit()
conn.close()