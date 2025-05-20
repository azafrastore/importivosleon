import streamlit as st
import os
import re

st.set_page_config(page_title="Importivos León", layout="wide")

# Encabezado con logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo Deportivo")

st.markdown("<p style='font-size:16px; color: gray;'>Calle 52 # 16-31 Barrio San Miguel</p>", unsafe_allow_html=True)


# Inicializar carrito en sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = []

# Función para agregar al carrito
def agregar_al_carrito(ref, talla, precio):
    for item in st.session_state.carrito:
        if item["referencia"] == ref and item["talla"] == talla:
            item["cantidad"] += 1
            item["subtotal"] = item["precio"] * item["cantidad"]
            return
    st.session_state.carrito.append({
        "referencia": ref,
        "talla": talla,
        "precio": precio,
        "cantidad": 1,
        "subtotal": precio
    })

# Función para quitar del carrito
def quitar_del_carrito(ref, talla):
    for item in st.session_state.carrito:
        if item["referencia"] == ref and item["talla"] == talla:
            item["cantidad"] -= 1
            if item["cantidad"] <= 0:
                st.session_state.carrito.remove(item)
            else:
                item["subtotal"] = item["precio"] * item["cantidad"]
            return

# CARRITO de compras
st.title("🛒 Carrito de compras")

col_vaciar, col_total = st.columns([1, 5])
with col_vaciar:
    if st.button("🗑️ Vaciar carrito"):
        st.session_state.carrito.clear()

with col_total:
    if st.session_state.carrito:
        for item in st.session_state.carrito:
            st.markdown(f"- {item['referencia']} Talla {item['talla']} x{item['cantidad']} → ${item['subtotal']:,}")
        total = sum(i["subtotal"] for i in st.session_state.carrito)
        st.success(f"**Total: ${total:,}**")
    else:
        st.info("Tu carrito está vacío.")

st.markdown("---")



# Cargar imágenes desde la carpeta
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

# Obtener todas las tallas
tallas_disponibles = set()
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        partes = nombre_archivo.split(" - ")
        if len(partes) != 3:
            continue
        _, tallas_str, _ = partes
        tallas = re.findall(r"(\d+)\(\d+\)", tallas_str)
        tallas_disponibles.update(tallas)
    except:
        continue

tallas_ordenadas = sorted(tallas_disponibles, key=int)
talla_seleccionada = st.selectbox("Filtrar por talla:", ["Todas"] + tallas_ordenadas)

# Mostrar catálogo
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        partes = nombre_archivo.split(" - ")
        if len(partes) != 3:
            continue

        referencia, tallas_str, precio = partes
        precio = int(precio)
        precio_formateado = f"${precio:,}"
        tallas_info = re.findall(r"(\d+)\((\d+)\)", tallas_str)
        tallas_dict = {t: int(c) for t, c in tallas_info}

        if talla_seleccionada != "Todas" and talla_seleccionada not in tallas_dict:
            continue

        col1, col2, col3 = st.columns([2, 3, 2])
        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)
        with col2:
            st.markdown(f"### {referencia}")
            for talla, stock in tallas_dict.items():
                if talla_seleccionada != "Todas" and talla != talla_seleccionada:
                    continue

                col_t1, col_t2, col_t3, col_t4 = st.columns([3, 1, 1, 1])
                with col_t1:
                    st.markdown(f"Talla {talla}: {stock} {'pares' if stock > 1 else 'par'}")
                with col_t2:
                    if st.button("➖ -1", key=f"remove_{referencia}_{talla}"):
                        quitar_del_carrito(referencia, talla)
                with col_t3:
                    if st.button("➕ +1", key=f"add_{referencia}_{talla}"):
                        agregar_al_carrito(referencia, talla, precio)
        with col3:
            st.markdown(f"<h4 style='color: green;'>{precio_formateado}</h4>", unsafe_allow_html=True)

        st.markdown("---")
    except Exception as e:
        st.warning(f"Error con archivo '{archivo}': {e}")
