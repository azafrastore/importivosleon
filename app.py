import streamlit as st
import os
import re

st.set_page_config(page_title="Importivos León", layout="wide")

# Inicializar sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = []

st.title("🛒 Carrito de compras")
if st.session_state.carrito:
    for item in st.session_state.carrito:
        st.markdown(f"- {item['referencia']} Talla {item['talla']} x{item['cantidad']} → ${item['subtotal']:,}")
    total = sum(item["subtotal"] for item in st.session_state.carrito)
    st.success(f"**Total: ${total:,}**")
else:
    st.info("Tu carrito está vacío.")

st.markdown("---")

# Logo y título
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo Deportivo")

st.markdown("<p style='font-size:16px; color: gray;'>Calle 52 # 16-31 Barrio San Miguel</p>", unsafe_allow_html=True)

# Carpeta del catálogo
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

# Extraer todas las tallas posibles
tallas_disponibles = set()
for archivo in imagenes:
    nombre_archivo = os.path.splitext(archivo)[0]
    try:
        partes = nombre_archivo.split(" - ")
        if len(partes) != 3:
            continue
        _, tallas_str, _ = partes
        tallas = re.findall(r"(\d+)\(\d+\)", tallas_str)
        tallas_disponibles.update(tallas)
    except:
        pass

tallas_ordenadas = sorted(tallas_disponibles, key=int)
talla_seleccionada = st.selectbox("Filtrar por talla:", ["Todas"] + tallas_ordenadas)

# Mostrar productos
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
            for talla, cantidad in tallas_dict.items():
                if talla_seleccionada != "Todas" and talla != talla_seleccionada:
                    continue
                col_t1, col_t2, col_t3 = st.columns([2, 1, 1])
                with col_t1:
                    st.markdown(f"Talla {talla}: {cantidad} {'pares' if cantidad > 1 else 'par'}")
                with col_t2:
                    cantidad_a_agregar = st.number_input(f"Cant {referencia}_{talla}", min_value=0, max_value=cantidad, step=1, label_visibility="collapsed", key=f"cant_{referencia}_{talla}")
                with col_t3:
                    if st.button("+", key=f"add_{referencia}_{talla}"):
                        if cantidad_a_agregar > 0:
                            subtotal = precio * cantidad_a_agregar
                            st.session_state.carrito.append({
                                "referencia": referencia,
                                "talla": talla,
                                "cantidad": cantidad_a_agregar,
                                "subtotal": subtotal
                            })
        with col3:
            st.markdown(f"<h4 style='color: green;'>{precio_formateado}</h4>", unsafe_allow_html=True)

        st.markdown("---")
    except Exception as e:
        st.warning(f"Error con archivo '{archivo}': {e}")
