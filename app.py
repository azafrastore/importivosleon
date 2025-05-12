import streamlit as st
import os

st.set_page_config(page_title="Catálogo de imágenes", layout="wide")
st.title("Catálogo de imágenes")

# Ruta relativa a la carpeta de imágenes dentro del repo
carpeta = "catalogo"
# Obtener lista de imágenes con extensiones válidas
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]

imagenes.sort()  # opcional, para mostrar en orden alfabético

# Mostrar las imágenes en tabla (imagen + título + precio)
for archivo in imagenes:
    try:
        # Separar título y precio usando el nombre del archivo
        nombre_archivo = os.path.splitext(archivo)[0]  # quita extensión
        titulo, precio = nombre_archivo.split(" - ")

        # Crear las columnas
        col1, col2, col3 = st.columns([2, 3, 1])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_column_width=True)

        with col2:
            st.markdown(f"### {titulo}")

        with col3:
            st.markdown(f"<h4 style='color: green;'>${precio}</h4>", unsafe_allow_html=True)

        st.markdown("---")  # Separador visual
    except ValueError:
        st.warning(f"El archivo '{archivo}' no tiene el formato esperado: 'nombre - precio.jpg'")
