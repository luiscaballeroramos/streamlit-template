import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = Path(__file__).resolve().parents[1] / "app.py"


class AppTests(unittest.TestCase):
    def test_home_loads_without_credentials(self):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Mi aplicacion")

    def test_example_page_loads(self):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        app.switch_page(str(Path("pages") / "example.py")).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.title[0].value, "Ejemplo")
        self.assertEqual(app.metric[0].value, "25")
        self.assertEqual(len(app.dataframe[0].value), 3)

    def test_layout_demo_keeps_state_between_distributions(self):
        app = AppTest.from_file(str(APP), default_timeout=15).run()
        app.switch_page(str(Path("pages") / "layout_demo.py")).run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.selectbox(key="demo-height").value, "Pantalla")
        app.text_input(key="demo-note").input("Conservar estado").run()
        for orientation in ("Vertical", "Horizontal", "Automatica"):
            app.selectbox(key="demo-orientation").select(orientation).run()
            self.assertEqual(len(app.exception), 0)
            self.assertEqual(app.text_input(key="demo-note").value, "Conservar estado")
        app.selectbox(key="demo-height").select("Fluida").run()
        self.assertEqual(len(app.exception), 0)
        app.selectbox(key="demo-variant").select("Principal destacado").run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.text_input(key="demo-note").value, "Conservar estado")
        app.checkbox(key="demo-long").check().run()
        self.assertEqual(len(app.exception), 0)
        self.assertTrue(any("Detalle 12:" in element.value for element in app.markdown))


if __name__ == "__main__":
    unittest.main()
