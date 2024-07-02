import streamlit as st
import pandas as pd

st.title('Cargar y mostrar archivo de Excel')

uploaded_file = st.file_uploader("Adjuntar archivo Excel", type=["xlsx", "xls"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Contenido del archivo:")
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error al leer el archivo: {e}")
