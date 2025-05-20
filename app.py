import streamlit as st
import os

st.set_page_config(page_title="Importivos León", layout="wide")

# Encabezado con logo y título
col1, col2 = st.columns([1, 5]) 

with col1:
    st.image("logo.png", width=150)  

with col2:
    st.title("Nuestro Catálogo Deportivo")

st.markdown("<p style='font-size:16px; color: gray;'>Calle 52 # 16-31 Barrio San Miguel</p>", unsafe_allow_html=True)

# Carpeta donde están las imágenes
carpeta = "catalogo"

# Soportar .jfif además de otras extensiones
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

# Función para formatear las tallas
def formatear_tallas(talla_str):
    tallas_separadas = talla_str.split(",")
    resultado = []
    for entrada in tallas_separadas:
        if "(" in entrada and ")" in entrada:
            talla, cantidad = entrada.strip().split("(")
            cantidad = cantidad.strip(")").strip()
            if cantidad.isdigit() and int(cantidad) > 0:
                plural = "par" if cantidad == "1" else "pares"
                resultado.append(f"{talla.strip()} - {cantidad} {plural}")
    return "<br>".join(resultado)

# Mostrar las imágenes en tabla (imagen + referencia + precio)
for archivo in imagenes:
    try:
        # Separar campos usando el nombre del archivo
        nombre_archivo = os.path.splitext(archivo)[0]  # sin extensión
        referencia, tallas, precio = nombre_archivo.split(" - ")

        precio_formateado = "{:,.0f}".format(int(precio))  # Formatear con separadores
        tallas_formateadas = formatear_tallas(tallas)

        # Crear columnas para mostrar
        col1, col2, col3 = st.columns([2, 3, 1])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)

        with col2:
            st.markdown(f"### {referencia}")
            st.markdown(tallas_formateadas, unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

        st.markdown("---") 

    except ValueError:
        st.warning(f"El archivo '{archivo}' no tiene el formato esperado: 'referencia - tallas - precio.jfif'")
