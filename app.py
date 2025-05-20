import streamlit as st
import os
import re

st.set_page_config(page_title="Importivos León", layout="wide")

# Inicializar carrito en la sesión
if "carrito" not in st.session_state:
    st.session_state["carrito"] = {}

# Encabezado
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo Deportivo")

st.markdown("<p style='font-size:16px; color: gray;'>Calle 52 # 16-31 Barrio San Miguel</p>", unsafe_allow_html=True)

# Mostrar el carrito arriba
st.subheader("🛒 Carrito de Compras")
carrito = st.session_state["carrito"]
if carrito:
    total = 0
    for (referencia, talla), cantidad in carrito.items():
        precio_unitario = st.session_state.get("precios", {}).get((referencia, talla), 0)
        subtotal = cantidad * precio_unitario
        total += subtotal
        st.write(f"{referencia} - Talla {talla} - {cantidad} par{'es' if cantidad > 1 else ''} - ${subtotal:,.0f}")
    st.success(f"Total: ${total:,.0f}")
    if st.button("Vaciar carrito"):
        st.session_state["carrito"] = {}
        st.experimental_rerun()
else:
    st.info("Tu carrito está vacío.")

st.markdown("---")

# Carpeta y filtro por talla
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

tallas_disponibles = sorted({t for img in imagenes for t in re.findall(r"(\d{2})\\(", img)})
opciones_filtro = ["Todas"] + tallas_disponibles

filtro_talla = st.selectbox("Filtrar por talla:", opciones_filtro)

# Mostrar imágenes
st.subheader("Catálogo")
st.session_state["precios"] = {}

for archivo in imagenes:
    nombre_archivo = os.path.splitext(archivo)[0]
    partes = nombre_archivo.split(" - ")

    if len(partes) != 3:
        st.warning(f"Formato no válido: {archivo}")
        continue

    referencia = partes[0].strip()
    tallas_raw = partes[1].strip()
    precio_str = partes[2].strip()

    try:
        precio = int(precio_str)
        precio_formateado = f"${precio:,.0f}"
    except ValueError:
        st.warning(f"Precio inválido: {archivo}")
        continue

    # Extraer tallas y cantidades
    tallas = re.findall(r"(\d{2})\\((\d+)\)", tallas_raw)
    tallas_filtradas = tallas if filtro_talla == "Todas" else [t for t in tallas if t[0] == filtro_talla]

    if not tallas_filtradas:
        continue

    # Mostrar en tabla
    col1, col2, col3 = st.columns([2, 3, 1])
    with col1:
        st.image(os.path.join(carpeta, archivo), use_container_width=True)
    with col2:
        st.markdown(f"### {referencia}")
        for talla, cantidad in tallas_filtradas:
            st.markdown(f"Talla {talla}: {cantidad} par{'es' if int(cantidad) > 1 else ''}")
            key = (referencia, talla)
            st.session_state["precios"][key] = precio

            bcol1, bcol2, bcol3 = st.columns([1, 1, 2])
            with bcol1:
                if st.button("➖", key=f"remove_{referencia}_{talla}"):
                    if key in st.session_state["carrito"]:
                        st.session_state["carrito"][key] -= 1
                        if st.session_state["carrito"][key] <= 0:
                            del st.session_state["carrito"][key]
                        st.experimental_rerun()
            with bcol2:
                if st.button("➕", key=f"add_{referencia}_{talla}"):
                    if key in st.session_state["carrito"]:
                        st.session_state["carrito"][key] += 1
                    else:
                        st.session_state["carrito"][key] = 1
                    st.experimental_rerun()
            with bcol3:
                st.markdown(f"Talla: **{talla}**")

    with col3:
        st.markdown(f"<h4 style='color: green;'>{precio_formateado}</h4>", unsafe_allow_html=True)

    st.markdown("---")
