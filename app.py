import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(layout='wide')
st.title("Analise de Estoque")
# Conectar ao banco de dados
conn = sqlite3.connect("estoque_produtos.db", check_same_thread=False)
cursor = conn.cursor()

st.title("📦 Controle de Estoque")

# Adicionar novo produto
st.sidebar.header("Adicionar Produto")
nome = st.sidebar.text_input("Nome do Produto")
sku = st.sidebar.text_input("SKU")
quantidade = st.sidebar.number_input("Quantidade Inicial", min_value=0, step=1)
if st.sidebar.button("Salvar Produto"):
    cursor.execute("INSERT INTO produtos (nome, sku, quantidade) VALUES (?, ?, ?)", (nome, sku, quantidade))
    conn.commit()
    st.sidebar.success("Produto adicionado!")

# Registrar entrada e saída
st.sidebar.header("Movimentação de Estoque")
produtos = pd.read_sql("SELECT id, nome FROM produtos", conn)
produto_selecionado = st.sidebar.selectbox("Produto", produtos["nome"] if not produtos.empty else [])
tipo_movimento = st.sidebar.radio("Tipo de Movimentação", ["entrada", "saida"])
quantidade_mov = st.sidebar.number_input("Quantidade", min_value=1, step=1)


if st.sidebar.button("Registrar Movimentação") and not produtos.empty:

    res = cursor.execute("SELECT SUM(quantidade) FROM produtos WHERE nome = ?", (produto_selecionado,))
    resultado = res.fetchone()[0]

    if quantidade_mov > resultado and tipo_movimento == "saida":
        st.sidebar.error("VALOR MAIOR QUE ESTOQUE!")

    else:
        produto_id: int = int(produtos.loc[produtos["nome"] == produto_selecionado, "id"].values[0])
        cursor.execute("INSERT INTO movimentacoes (produto_id, tipo, quantidade) VALUES (?, ?, ?)",
                       (produto_id, tipo_movimento, quantidade_mov))
        conn.commit()

        if tipo_movimento == "entrada":
            cursor.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade_mov, produto_id))
            conn.commit()
        else:
            cursor.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ? ", (quantidade_mov, produto_id))
            conn.commit()
        st.sidebar.success("Movimentação registrada!")


# Exibir produtos
st.subheader("📋 Estoque Atual")
df_produtos = pd.read_sql("SELECT * FROM produtos", conn)
st.table(df_produtos)

# Exibir movimentações
st.subheader("📊 Histórico de Movimentações")
df_movimentacoes = pd.read_sql(
    "SELECT movimentacoes.id, produtos.nome AS produto, movimentacoes.tipo, movimentacoes.quantidade, movimentacoes.data "
    "FROM movimentacoes JOIN produtos ON movimentacoes.produto_id = produtos.id ORDER BY movimentacoes.data DESC", conn)
st.table(df_movimentacoes)
