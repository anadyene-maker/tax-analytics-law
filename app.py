import streamlit as st
import pandas as pd
import numpy as np

# 1. Configurações Iniciais da Página
st.set_page_config(page_title="Tax Analytics - Indústria MS", layout="wide")

# Estilo para o título
st.title("⚖️ Sistema de Auditoria Fiscal e Logística")
st.markdown("""
Esta ferramenta analisa o impacto tributário de saídas de mercadorias partindo de **Mato Grosso do Sul** 
para todo o Brasil, comparando alíquotas e identificando potencial de crédito.
""")

# 2. Banco de Dados de Alíquotas Interestaduais (Origem: MS)
# Fonte: Regulamento do ICMS / Convênio ICMS
regras_estados = {
    'AC': 12.0, 'AL': 12.0, 'AM': 12.0, 'AP': 12.0, 'BA': 12.0, 'CE': 12.0,
    'DF': 12.0, 'ES': 12.0, 'GO': 12.0, 'MA': 12.0, 'MG': 7.0, 'MS': 17.0, 
    'MT': 12.0, 'PA': 12.0, 'PB': 12.0, 'PE': 12.0, 'PI': 12.0, 'PR': 7.0, 
    'RJ': 7.0, 'RN': 12.0, 'RO': 12.0, 'RR': 12.0, 'RS': 7.0, 'SC': 7.0, 
    'SE': 12.0, 'SP': 7.0, 'TO': 12.0
}

# 3. Barra Lateral para Instruções e Parâmetros Fixos
with st.sidebar:
    st.header("Configurações")
    st.info("O sistema utiliza MS como estado de origem padrão.")
    aliq_pis_cofins = st.number_input("Alíquota PIS/COFINS (%)", value=9.25) / 100
    st.write("---")
    st.markdown("Desenvolvido por **Ana Dyene Pires**")

# 4. Área de Upload de Arquivos
uploaded_files = st.file_uploader(
    "Arraste aqui os relatórios de vendas/logística das filiais", 
    type=["csv", "xlsx"], 
    accept_multiple_files=True
)

# 5. Processamento dos Dados
if uploaded_files:
    lista_comparativa = []

    for file in uploaded_files:
        # Lendo o arquivo conforme a extensão
        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Padronizando nomes das colunas (exemplo: remover espaços)
            df.columns = df.columns.str.strip()

            # Verificando se as colunas necessárias existem no arquivo subido
            if 'Estado' in df.columns and 'Valor_Venda' in df.columns:
                
                # Mapeando a alíquota de ICMS baseada no Estado de destino
                df['Aliq_ICMS'] = df['Estado'].map(regras_estados).fillna(17.0)
                
                # Cálculos Tributários
                df['ICMS_Estimado'] = df['Valor_Venda'] * (df['Aliq_ICMS'] / 100)
                df['Credito_PIS_COFINS'] = df['Valor_Venda'] * aliq_pis_cofins
                
                # Consolidando resultados por arquivo (filial)
                total_venda = df['Valor_Venda'].sum()
                total_icms = df['ICMS_Estimado'].sum()
                total_credito = df['Credito_PIS_COFINS'].sum()
                
                lista_comparativa.append({
                    "Unidade/Arquivo": file.name.split('.')[0],
                    "Volume de Vendas": total_venda,
                    "ICMS Provisionado": total_icms,
                    "Crédito Recuperável": total_credito
                })
            else:
                st.warning(f"⚠️ O arquivo {file.name} não possui as colunas 'Estado' e 'Valor_Venda'.")
        
        except Exception as e:
            st.error(f"Erro ao processar {file.name}: {e}")

    # 6. Exibição dos Dashboards
    if lista_comparativa:
        df_final = pd.DataFrame(lista_comparativa)
        
        st.subheader("📊 Comparativo Gerencial entre Filiais")
        
        # Formatação de Moeda para a tabela
        st.dataframe(df_final.style.format({
            "Volume de Vendas": "R$ {:,.2f}",
            "ICMS Provisionado": "R$ {:,.2f}",
            "Crédito Recuperável": "R$ {:,.2f}"
        }), use_container_width=True)

        st.divider()

        # Gráficos
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Crédito Recuperável por Unidade**")
            st.bar_chart(data=df_final.set_index('Unidade/Arquivo')['Crédito Recuperável'])
        
        with col2:
            st.write("**Carga de ICMS Estimada**")
            st.line_chart(data=df_final.set_index('Unidade/Arquivo')['ICMS Provisionado'])

        # Botão de Exportação do Consolidado
        st.download_button(
            label="📩 Baixar Relatório Consolidado (CSV)",
            data=df_final.to_csv(index=False).encode('utf-8'),
            file_name='consolidado_tax_analytics.csv',
            mime='text/csv'
        )
else:
    st.info("Aguardando o upload de arquivos CSV ou Excel para gerar o relatório.")
