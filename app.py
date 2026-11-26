from pathlib import Path

import streamlit as st


def main() -> None:
    st.set_page_config(page_title="Mi aplicacion", layout="wide")
    navigation = st.navigation([
        st.Page(Path("pages") / "home.py", title="Inicio", default=True),
        st.Page(Path("pages") / "example.py", title="Ejemplo", url_path="ejemplo"),
        st.Page(Path("pages") / "layout_demo.py", title="Laboratorio de espacios", url_path="espacios"),
    ])
    navigation.run()


if __name__ == "__main__":
    main()
