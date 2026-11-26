import streamlit as st

from layouts import Layout, render_layout


HORIZONTAL = Layout(
    areas=(("filters", "main", "details"),),
    columns=(20, 60, 20), rows=(100,),
)
VERTICAL = Layout(
    areas=(("filters",), ("main",), ("details",)),
    columns=(100,), rows=(20, 55, 25), min_height=600,
)
HORIZONTAL_ALTERNATIVE = Layout(
    areas=(("main", "filters"), ("main", "details")),
    columns=(70, 30), rows=(40, 60), min_height=400,
)
VERTICAL_ALTERNATIVE = Layout(
    areas=(("main",), ("filters",), ("details",)),
    columns=(100,), rows=(60, 20, 20), min_height=600,
)

with st.sidebar:
    st.subheader("Laboratorio")
    variant = st.selectbox("Ejemplo", ["Tres zonas", "Principal destacado"], key="demo-variant")
    orientation = st.selectbox(
        "Distribucion", ["Automatica", "Horizontal", "Vertical"], key="demo-orientation",
    )
    height_mode = st.selectbox("Altura", ["Pantalla", "Fluida"], key="demo-height")


def header() -> None:
    st.title("Laboratorio de espacios")
    st.caption("Mismo contenido, dos layouts explicitos. Configuracion en el menu lateral.")


def filters() -> None:
    st.subheader("Filtros")
    st.selectbox("Categoria", ["Todas", "A", "B"], key="demo-category")


def main_content() -> None:
    st.subheader("Contenido principal")
    st.write(f"Categoria seleccionada: **{st.session_state.get('demo-category', 'Todas')}**")
    st.text_input("Escribe algo y cambia de orientacion", key="demo-note")
    st.slider("Cantidad", 1, 100, 25, key="demo-count")
    st.info("Los controles se crean una sola vez; la distribucion cambia mediante CSS.")


def details() -> None:
    st.subheader("Detalles")
    if st.checkbox("Mostrar texto largo", key="demo-long"):
        for index in range(12):
            st.write(f"Detalle {index + 1}: contenido de prueba para comprobar el desplazamiento.")
    else:
        st.write("Activa el texto largo para probar el contenido que no cabe.")


alternative = variant == "Principal destacado"
render_layout(
    key="demo",
    horizontal=HORIZONTAL_ALTERNATIVE if alternative else HORIZONTAL,
    vertical=VERTICAL_ALTERNATIVE if alternative else VERTICAL,
    regions={"filters": filters, "main": main_content, "details": details},
    header=header,
    orientation={"Automatica": "auto", "Horizontal": "horizontal", "Vertical": "vertical"}[orientation],
    height="screen" if height_mode == "Pantalla" else "fluid",
)
