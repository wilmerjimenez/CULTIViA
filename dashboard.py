import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import openai

st.set_page_config(layout="wide")

# --- Pestaña lateral de chatbot ---
st.sidebar.title("🤖 CULTIViA Chatbot")
openai.api_key = st.sidebar.text_input("Introduce tu API Key de OpenAI", type="password")
user_input = st.sidebar.text_area("Consulta al sistema (en español o inglés):")

if st.sidebar.button("Enviar") and openai.api_key and user_input:
    with st.spinner("Pensando..."):
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}]
        )
        st.sidebar.markdown("**Respuesta:**")
        st.sidebar.success(respuesta.choices[0].message.content.strip())

# --- Cuerpo principal del dashboard ---
def cargar_datos():
    conn = sqlite3.connect('cultivia.db')
    df = pd.read_sql_query("SELECT * FROM clima", conn)
    conn.close()
    return df

df = cargar_datos()
st.title("🌱 CULTIViA - Monitoreo Climático en Ecuador")

fig = px.line(df, x='fecha', y=['precipitacion', 'spi', 'spei'], title='Índices de sequía y precipitaciones')
st.plotly_chart(fig)

alertas = df[df['alerta'] != '']
st.subheader("🔔 Alertas recientes")
st.dataframe(alertas[['fecha', 'alerta']])
