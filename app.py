import streamlit as st
import pandas as pd
import numpy as np

# Configuração visual do Dashboard
st.set_page_config(page_title="Legal Analytics - Indústria de Snacks", layout="wide")

st.title("⚖️ Tax Profit Finder: Auditoria de Créditos (PIS/COFINS)")
st.markdown("""
Este dashboard demonstra a aplicação da **Tese da Essencialidade (STJ)** para identificar créditos tributários 
não aproveitados em uma indústria de snacks.
""")

# 1. Simulação de Dados Reais de uma Indústria de Snacks (Semalo-style)
def generate_industry_data():
    data = {
        'Insumo/Despesa': [
            'Milho em Grãos (Matéria-prima)', 
            'Óleo de Palma para Fritura', 
            'Temperos e Condimentos', 
            'Embalagens de Polipropileno (BOPP)', 
            'Energia Elétrica (Linha de Produção)', 
            'Manutenção Preventiva de Extrusoras',
            'Frete de Venda (Saída)', 
            'Uniformes da Equipe de Fábrica',
            'Material de Limpeza Administrativo',
            'Combustível Frota de Vendas'
        ],
        'Valor_Compra': [450000, 180000, 45000, 120000, 85000, 25000, 60000, 8000, 3500, 15000],
        'Natureza': [
            'Direto', 'Direto', 'Direto', 'Direto', 
            'Essencial', 'Essencial', 'Logística', 
            'Essencial', 'Adm', 'Vendas'
        ]
    }
    return pd.DataFrame(data)

df = generate_industry_data()

# 2. Lógica Jurídica (Alíquota Modal de 9,25% para Lucro Real)
aliquota = 0.0925

# Regra: Insumos Diretos, Essenciais e Fretes de Venda costumam gerar crédito
df['Geraria_Credito'] = df['Natureza'].apply(
    lambda x: 'Sim' if x in ['Direto', 'Essencial', 'Logística'] else 'Não'
)
df['Valor_Credito'] = np.where(df['Geraria_Credito'] == 'Sim', df['Valor_Compra'] * aliquota, 0)

# 3. Interface do Usuário
st.subheader("🔍 Mapeamento de Insumos Industriais")
st.dataframe(df.style.format({"Valor_Compra": "R$ {:,.2f}", "Valor_Credito": "R$ {:,.2f}"}))

# 4. Resultados Financeiros
total_recuperavel = df['Valor_Credito'].sum()

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.metric("Crédito Potencial Identificado", f"R$ {total_recuperavel:,.2f}")
    st.write("**Explicação Jurídica:**")
    st.caption("""
    A análise considera que o frete de venda e os uniformes (EPIs) são essenciais para a 
    atividade econômica, conforme o entendimento ampliado de 'insumo' pelo STJ.
    """)

with col2:
    st.bar_chart(data=df.set_index('Insumo/Despesa')['Valor_Credito'])

st.success("✅ Este projeto demonstra como o Direito Tributário Preventivo pode gerar lucro direto para a indústria.")
