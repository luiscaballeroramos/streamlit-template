import streamlit as st


st.title("Ejemplo")
st.caption("Datos ficticios incluidos en la plantilla. No requieren credenciales.")
rows = [
    {"Categoria": "A", "Cantidad": 12},
    {"Categoria": "B", "Cantidad": 8},
    {"Categoria": "C", "Cantidad": 5},
]
st.metric("Total de elementos", sum(row["Cantidad"] for row in rows))
st.dataframe(rows, hide_index=True, width="stretch")
