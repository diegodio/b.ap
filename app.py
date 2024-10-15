import streamlit as st
import requests
import json
import datetime
import pandas as pd
import plotly.graph_objects as go


LINK = "https://homefinanceteste-default-rtdb.firebaseio.com/"


st.title('b.AP')



tab1, tab2 = st.tabs(["Informações", "Postar"])

# Condição para o conteúdo da página
with tab1:
    st.write('Teste')
    if st.button('Carregar'):
        requisicao = requests.get(f'{LINK}/Pagamentos/.json')

        if requisicao.status_code != 200:
            st.write(f'Código {requisicao.status_code} - Ops, algo deu errado!')
        else:
            st.write(f'Código {requisicao.status_code} - Carregamento realizado com sucesso!')

            dic_requisicao = requisicao.json()

            df = pd.DataFrame(dic_requisicao)
            st.write(f'Total pago: R${df.T["Valor pago"].sum()}')
            st.write(f'Total pago: {df.T["Valor pago"].sum() * 100 / 200000:.2f}%')


            

            # Dados de exemplo
            labels = ['Pago', 'A pagar']
            values = [df.T["Valor pago"].sum(), 200000-df.T["Valor pago"].sum()]

            # Criação do gráfico
            fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.8)])

            fig.update_traces(textinfo='percent', texttemplate='%{percent:.2%}')

            # Título do gráfico
            fig.update_layout(title_text='Gráfico de Donut')

            # Exibe o gráfico
            st.plotly_chart(fig)



with tab2:
    data_selecionada = st.date_input('Data da parcela', datetime.date.today(), format="DD/MM/YYYY")
    valor_parcela = st.number_input("Valor parcela", format="%d", step=100)
    if st.button('Postar'):
        dados = {'Data': str(data_selecionada), 'Valor pago': valor_parcela}
        requisicao = requests.post(f'{LINK}/Pagamentos/.json', data=json.dumps(dados))
        if requisicao.status_code == 200:
            st.write(f'Código {requisicao.status_code} - Postagem realizada com sucesso!')
        else:
            st.write(f'Código {requisicao.status_code} - Ops, algo deu errado!')

