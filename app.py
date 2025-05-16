
import streamlit as st
from gerador_megasena import gerar_cartoes
from util import exportar_pdf, exportar_txt
from mega_estatisticas import (
    obter_estatisticas_basicas,
    dezenas_mais_sorteadas,
    dezenas_menos_sorteadas,
    pares_impares,
    soma_dezenas,
    distribuicao_linha_coluna,
    graficos_estatisticos
)
import matplotlib.pyplot as plt

def ler_ultimo_resultado():
    try:
        with open("resultados.txt", "r") as f:
            return sorted([int(x) for x in f.read().strip().split()])
    except:
        return []

def comparar_com_ultimo(cartao, resultado):
    acertos = set(cartao) & set(resultado)
    return sorted(acertos), len(acertos)

st.set_page_config(page_title="Mega-Sena Inteligente V2", layout="wide")
st.title("🎯 Mega-Sena Inteligente V2")

tab1, tab2, tab3, tab4 = st.tabs(["🎰 Gerar Jogos", "📊 Estatísticas", "🔍 Verificar Jogo", "📥 Exportar"])

with tab1:
    st.header("Gerador de Jogos")
    quantidade = st.slider("Quantos cartões deseja gerar?", 1, 10, 1)
    if "historico" not in st.session_state:
        st.session_state.historico = []
    if st.button("Gerar Cartões"):
        cartoes = gerar_cartoes(quantidade)
        st.session_state.historico.extend(cartoes)
        resultado = ler_ultimo_resultado()
        for i, cartao in enumerate(cartoes, start=1):
            texto = f"Cartão {i}: {' - '.join(f'{n:02}' for n in cartao)}"
            if resultado:
                acertos, qtd = comparar_com_ultimo(cartao, resultado)
                texto += f" | 🎯 {qtd} acertos: {', '.join(map(str, acertos)) if acertos else 'nenhum'}"
            st.success(texto)

with tab2:
    st.header("📊 Estatísticas dos Resultados")
    resultado = ler_ultimo_resultado()
    if resultado:
        st.subheader("Último resultado:")
        st.info(" - ".join(str(n) for n in resultado))

        st.subheader("Análise rápida:")
        st.write(pares_impares(resultado))
        st.write(soma_dezenas(resultado))
        st.write(distribuicao_linha_coluna(resultado))

        st.subheader("Gráficos:")
        fig = graficos_estatisticos()
        st.pyplot(fig)
    else:
        st.warning("Nenhum resultado encontrado em resultados.txt")

with tab3:
    st.header("🔍 Verificar Jogo Manualmente")
    numeros = st.text_input("Digite 6 dezenas separadas por espaço:", "")
    if numeros:
        try:
            cartao = sorted([int(n) for n in numeros.strip().split()])
            if len(cartao) != 6:
                st.error("Você deve informar exatamente 6 dezenas.")
            else:
                resultado = ler_ultimo_resultado()
                acertos, qtd = comparar_com_ultimo(cartao, resultado)
                st.success(f"Você teve {qtd} acerto(s): {', '.join(map(str, acertos)) if acertos else 'nenhum'}")
        except:
            st.error("Erro ao interpretar os números. Verifique se estão separados corretamente.")

with tab4:
    st.header("📥 Exportar Jogos")
    if st.session_state.historico:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Exportar .TXT"):
                caminho = exportar_txt(st.session_state.historico)
                st.success(f"Arquivo salvo como: {caminho}")
        with col2:
            if st.button("Exportar .PDF"):
                caminho = exportar_pdf(st.session_state.historico)
                st.success(f"Arquivo salvo como: {caminho}")
    else:
        st.info("Gere pelo menos um cartão para exportar.")
