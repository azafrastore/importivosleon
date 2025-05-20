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

# -------- Filtro por talla --------
# Buscar todas las tallas existentes
tallas_disponibles = set()
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        _, tallas_raw, _ = nombre_archivo.split(" - ")
        tallas_partes = tallas_raw.split(",")
        for entrada in tallas_partes:
            if "(" in entrada:
                talla = entrada.strip().split("(")[0].strip()
                tallas_disponibles.add(talla)
    except Exception:
        continue

# Convertir a lista ordenada
tallas_opciones = sorted(list(tallas_disponibles))
talla_seleccionada = st.multiselect("Filtrar por talla", ["Todas las tallas"] + tallas_opciones, default=["Todas las tallas"])

def mostrar_producto(referencia, tallas, precio, archivo):
    precio_formateado = "{:,.0f}".format(int(precio))

    # Procesar tallas con formato "38 - 2 pares"
    tallas_separadas = tallas.split(",")
    resultado_tallas = []
    tallas_en_producto = set()
    for entrada in tallas_separadas:
        if "(" in entrada:
            talla, cantidad = entrada.strip().split("(")
            talla = talla.strip()
            cantidad = cantidad.strip(")").strip()
            if cantidad.isdigit() and int(cantidad) > 0:
                plural = "par" if cantidad == "1" else "pares"
                resultado_tallas.append(f"{talla} - {cantidad} {plural}")
                tallas_en_producto.add(talla)

    # Verificar si mostrar o no este producto según el filtro
    if "Todas las tallas" in talla_seleccionada or any(t in tallas_en_producto for t in talla_seleccionada):
        col1, col2, col3 = st.columns([2, 3, 1])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)

        with col2:
            st.markdown(f"### {referencia}")
            st.markdown("<br>".join(resultado_tallas), unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

        st.markdown("---")

# -------- Mostrar catálogo filtrado --------
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        referencia, tallas_raw, precio = nombre_archivo.split(" - ")
        mostrar_producto(referencia, tallas_raw, precio, archivo)
    except ValueError:
        st.warning(f"El archivo '{archivo}' no tiene el formato esperado: 'referencia - tallas - precio.ext'")
