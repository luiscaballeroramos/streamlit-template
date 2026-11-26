# streamlit-template

Base independiente para aplicaciones Streamlit. Funciona sin credenciales,
servicios externos ni datos de otros proyectos.

## Requisitos

- Python 3.10 o posterior.
- Ejecutar los comandos desde la carpeta del proyecto.

## Preparacion en Windows

```powershell
git clone https://github.com/luiscaballeroramos/streamlit-template.git
Set-Location streamlit-template
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Ejecutar

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Streamlit muestra la direccion local en la terminal. Para detenerlo, pulsa
Ctrl+C. No es necesario activar el entorno virtual.

## Pruebas sin red

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Las pruebas comprueban las paginas, el estado de los controles y las reglas
de las distribuciones.

## Personalizacion inicial

- Cambia los titulos y las paginas en [app.py](app.py).
- Edita el contenido de cada pagina en [pages/](pages/).
- Ajusta los colores en [.streamlit/config.toml](.streamlit/config.toml).
- Sustituye los datos ficticios de la pagina Ejemplo por tu funcionalidad.
- Si necesitas secretos, usa `.streamlit/secrets.toml` localmente o los
  secretos de la plataforma de despliegue. Nunca los guardes en el codigo.

El repositorio incluye la aplicacion de ejemplo y la API de layouts.
No configura despliegues automaticamente ni tiene dependencias de Spotify.

## Prototipo de distribucion

Abre **Laboratorio de espacios**. Tiene dos layouts explicitos:
horizontal (anchos 20/60/20) y vertical (altos 20/55/25), aplicados a los mismos
contenedores. Los porcentajes reparten el espacio despues de descontar las
separaciones. Automatica usa la orientacion de la ventana, no del dispositivo.
Puedes forzar ambas distribuciones para compararlas.

Pantalla es el modo inicial: las zonas usan desplazamiento interno. La altura
minima del marco es 600 px; en ventanas menores se permite desplazar la pagina
en vez de reducir los controles hasta hacerlos ilegibles. Fluida permite que
la pagina crezca. El layout vertical reserva al menos 600 px para sus zonas,
ademas de la cabecera; sus filas reparten ese espacio en las proporciones
indicadas. Si no cabe todo, la pagina puede desplazarse.

## Layouts reutilizables

[layouts.py](layouts.py) contiene una primera API pequena. Cada `Layout` define
una matriz de zonas, pesos de columnas y filas y altura minima del contenido.
Los pesos no tienen que sumar 100: `(1, 3, 1)` equivale a `(20, 60, 20)`.
Una zona puede ocupar varias celdas, siempre formando un rectangulo.

```python
from layouts import Layout, render_layout
import streamlit as st

render_layout(
    key="report",
    horizontal=Layout((("main", "details"),), (70, 30), (1,)),
    vertical=Layout((("main",), ("details",)), (1,), (75, 25), min_height=500),
    regions={
        "main": lambda: st.write("Contenido"),
        "details": lambda: st.write("Detalles"),
    },
)
```

Los dos layouts deben declarar exactamente las mismas zonas que `regions`.
El contenido se ejecuta una vez en el orden de `regions`; este tambien es el
orden de lectura y teclado, aunque CSS cambie la posicion visual. Conviene
mantener un orden semantico coherente en ambas orientaciones.

`orientation` admite `"auto"`, `"horizontal"` y `"vertical"`.
`height` admite `"screen"` (predeterminado) y `"fluid"`. En modo fluido las
filas crecen con el contenido: los porcentajes de alto no se aplican.
`header` permite pasar una funcion para la cabecera dentro del marco.

El laboratorio incluye un segundo ejemplo con una zona principal que ocupa
dos filas y un orden vertical diferente. Los controles de prueba estan en
la barra lateral, fuera del area repartida.

### Limites actuales

- El marco descuenta 5.75 rem de la altura de ventana para la interfaz de
  Streamlit y margenes; no mide dinamicamente barras personalizadas externas.
- La altura minima del marco es 600 px. Si cabecera y zonas necesitan mas
  espacio, se permite desplazar la pagina.
- Los minimos de contenido se definen por layout. En modo pantalla cada zona
  permite scroll interno; no se ocultan zonas por ser una ventana estrecha.
- El CSS queda acotado por la clave del layout, pero usa selectores internos
  de Streamlit. Hay que validar en navegador al cambiar su version.
- La API es inicial: se puede instalar desde este repositorio,
  pero no esta publicada en PyPI.

## Importar desde otra aplicacion

Con este repositorio en una carpeta hermana, instala una dependencia editable
en el entorno de la aplicacion consumidora:

```powershell
python -m pip install -e ..\streamlit-template
```

```python
from streamlit_template import Layout, render_layout
```

La instalacion editable utiliza directamente [layouts.py](layouts.py), sin
copiarlo en cada aplicacion. Reinicia Streamlit tras cambiar el modulo compartido.
La configuracion de empaquetado mantiene el codigo en la raiz; las paginas y
pruebas de la aplicacion de ejemplo siguen usando su import local existente.
