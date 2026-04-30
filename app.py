import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Auditoria Multi-Filiais", layout="wide")

st.title("⚖️ Auditoria Tributária - Comparativo entre Filiais/Cidades")
st.markdown("""
Suba os arquivos de diferentes unidades (ex: Campo Grande, Dourados, Três Lagoas) para comparar o potencial de crédito.
""")

# 1. Upload de Múltiplos Arquivos
uploaded_files = st.file_uploader(
    "Selecione os relatórios das filiais (CSV ou Excel)", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

# Alíquota de PIS/COFINS (9,25%)
aliquota = 0.0925

if uploaded_files:
    resultados_finais = []

    for file in uploaded_files:
        # Lógica para ler cada arquivo individualmente
        if file.name.endswith('.csv'):
            df_filial = pd.read_csv(file)
        else:
            df_filial = pd.read_excel(file)
        
        # Simulação de processamento: calculando crédito por filial
        # (Aqui o script procuraria as colunas de valor e natureza)
        if 'Valor_Compra' in df_filial.columns:
            credito_filial = df_filial['Valor_Compra'].sum() * aliquota
            resultados_finais.append({
                "Filial/Cidade": file.name.split('.')[0], # Usa o nome do arquivo como nome da filial
                "Total Compras": df_filial['Valor_Compra'].sum(),
                "Crédito Recuperável": credito_filial
            })

    # 2. Exibição da Comparação
    if resultados_finais:
        df_comparativo = pd.DataFrame(resultados_finais)
        
        st.subheader("📊 Resumo Comparativo")
        st.dataframe(df_comparativo.style.format({
            "Total Compras": "R$ {:,.2f}", 
            "Crédito Recuperável": "R$ {:,.2f}"
        }))

        # Gráfico de comparação entre as unidades
        st.bar_chart(data=df_comparativo.set_index('Filial/Cidade')['Crédito Recuperável'])

        st.success(f"Análise concluída para {len(uploaded_files)} unidades.")
else:
    st.info("Aguardando upload de arquivos para iniciar a comparação.")
