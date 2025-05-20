import streamlit as st
import os
import re

st.set_page_config(page_title="Importivos León", layout="wide")

# Inicializar el carrito en session_state si no existe
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

carpeta = "catalogo"

# Soportar .jfif además de otras extensiones
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]

imagenes.sort()

# Extraer tallas únicas de todos los archivos
tallas_disponibles = sorted({t for img in imagenes for t in re.findall(r"(\d{2})\(", img)})

# FILTRO por talla
talla_seleccionada = st.selectbox("Filtrar por talla", ["Todas"] + tallas_disponibles)

# --- Funciones para carrito ---

def agregar_al_carrito(ref, talla, cantidad):
    key = f"{ref}_{talla}"
    if key in st.session_state.carrito:
        st.session_state.carrito[key] += cantidad
    else:
        st.session_state.carrito[key] = cantidad
    if st.session_state.carrito[key] <= 0:
        del st.session_state.carrito[key]

def vaciar_carrito():
    st.session_state.carrito = {}

# --- Mostrar carrito arriba ---
st.header("Carrito de compras")

if not st.session_state.carrito:
    st.write("El carrito está vacío")
else:
    total = 0
    for key, cantidad in st.session_state.carrito.items():
        ref, talla = key.rsplit("_", 1)
        # Buscar precio en las imágenes para este ref
        precio = None
        for img in imagenes:
            nombre_archivo = os.path.splitext(img)[0]
            partes = nombre_archivo.split(" - ")
            if len(partes) >= 3:
                referencia = partes[0].strip()
                if referencia == ref:
                    try:
                        precio = int(partes[-1])
                    except:
                        precio = 0
                    break
        if precio is None:
            precio = 0
        subtotal = precio * cantidad
        total += subtotal
        precio_formateado = "{:,.0f}".format(precio)
        st.write(f"{ref} - Talla {talla}: {cantidad} pares x ${precio_formateado} = ${subtotal:,}")

    st.markdown(f"**Total: ${total:,}**")

if st.button("Vaciar carrito"):
    vaciar_carrito()

st.markdown("---")

# Mostrar catálogo
st.markdown("<h2>Catálogo de Zapatos</h2>", unsafe_allow_html=True)

for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]  # quita extensión
        partes = nombre_archivo.split(" - ")
        if len(partes) < 3:
            st.warning(f"El archivo '{archivo}' no tiene el formato esperado: 'referencia - tallas - precio.ext'")
            continue

        referencia = partes[0].strip()
        tallas_str = partes[1].strip()  # ej: "37(1),38(2),39(3)"
        precio_str = partes[2].strip()
        precio = int(precio_str)

        # Parsear tallas y cantidades
        tallas = re.findall(r"(\d{2})\((\d+)\)", tallas_str)  # lista de tuples (talla, cantidad)

        # Filtrar por talla seleccionada
        if talla_seleccionada != "Todas" and not any(t == talla_seleccionada for t, _ in tallas):
            continue

        # Mostrar cada producto en 3 columnas
        col1, col2, col3 = st.columns([2, 4, 1])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)

        with col2:
            st.markdown(f"### {referencia}")
            for t, c in tallas:
                st.markdown(f"Talla {t}: {c} pares")

        with col3:
            precio_formateado = "{:,.0f}".format(precio)
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

            # Mostrar botones para modificar cantidad en carrito por talla
            for t, c in tallas:
                key_minus = f"menos_{referencia}_{t}"
                key_plus = f"mas_{referencia}_{t}"
                cantidad_actual = st.session_state.carrito.get(f"{referencia}_{t}", 0)

                cols = st.columns([1, 1, 2])  # para botones y mostrar cantidad

                with cols[0]:
                    if st.button("-1", key=key_minus):
                        if cantidad_actual > 0:
                            agregar_al_carrito(referencia, t, -1)

                with cols[1]:
                    if st.button("+1", key=key_plus):
                        agregar_al_carrito(referencia, t, 1)

                with cols[2]:
                    st.write(f"Cantidad: {cantidad_actual}")

        st.markdown("---")

    except Exception as e:
        st.warning(f"Error con el archivo '{archivo}': {e}")
