import streamlit as st
import os

st.set_page_config(page_title="Importivos León", layout="wide")

# Crear las columnas para el logo y título
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo.png", width=150)  # Cambia "logo.png" con la ruta correcta del logo

with col2:
    st.title("Nuestro Catálogo Deportivo")

# Dirección debajo del título
st.markdown("<p style='font-size:16px; color: gray;'>Calle 52 # 16-31 Barrio San Miguel</p>", unsafe_allow_html=True)

# Ruta de la carpeta de imágenes dentro del repositorio
carpeta = "catalogo"

# Soportar .jfif además de otras extensiones
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]

imagenes.sort()

# Mostrar las imágenes en tabla (imagen + referencia + cantidades + precio)
for archivo in imagenes:
    try:
        # Separar referencia, tallas y precio usando el nombre del archivo
        nombre_archivo = os.path.splitext(archivo)[0]  # Quita la extensión
        referencia, tallas, precio = nombre_archivo.split(" - ")

        # Formatear el precio con separadores de miles
        precio_formateado = "{:,.0f}".format(int(precio))  # Convierte el precio en un número y lo formatea

        # Formatear las tallas
        tallas_formateadas = tallas.replace(",", "<br>").replace("(", " ").replace(")", " piezas")

        # Crear las columnas para imagen, referencia y cantidades, y precio
        col1, col2, col3 = st.columns([2, 3, 1])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)

        with col2:
            st.markdown(f"### {referencia}")
            st.markdown(f"**Tallas y cantidades:**<br>{tallas_formateadas}", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

        st.markdown("---")  # Separador visual

    except ValueError:
        st.warning(f"El archivo '{archivo}' no tiene el formato esperado: 'referencia - tallas - precio.jfif'")
