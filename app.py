import streamlit as st
import os
import re
import urllib.parse

st.set_page_config(page_title="Importivos León", layout="wide")

# Inicializar carrito y tallas seleccionadas en la sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = {}
if "tallas_seleccionadas" not in st.session_state:
    st.session_state.tallas_seleccionadas = {}  # producto_id -> talla seleccionada

# Encabezado con logo y título
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo Deportivo")

st.markdown("<p style='font-size:16px; color: gray;'>Bucaramanga</p>", unsafe_allow_html=True)

# Mostrar carrito
st.markdown("## 🛒 Carrito de compras")
if st.session_state.carrito:
    total = 0
    for key, item in st.session_state.carrito.items():
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{item['referencia']}** (Talla {item['talla']})")
        with col2:
            st.markdown(f"{item['cantidad']} unidad(es)")
        with col3:
            st.markdown(f"${subtotal:,.0f}".replace(",", "."))

    st.success(f"**Total a pagar:** ${total:,.0f}".replace(",", "."))
    if st.button("🩹 Vaciar carrito"):
        st.session_state.carrito.clear()
        st.session_state.tallas_seleccionadas.clear()
else:
    st.info("Tu carrito está vacío.")

# Botón WhatsApp
if st.session_state.carrito:
    mensaje = "Hola, quiero hacer el siguiente pedido:\n\n"
    total = 0
    for item in st.session_state.carrito.values():
        mensaje += f"- {item['referencia']} (Talla: {item['talla']}) x {item['cantidad']}\n"
        total += item['cantidad'] * item['precio']
    mensaje += f"\nTotal: ${total:,.0f}"

    mensaje_codificado = urllib.parse.quote(mensaje)
    numero_whatsapp = "+573115225576"
    url_whatsapp = f"https://api.whatsapp.com/send?phone={numero_whatsapp}&text={mensaje_codificado}"

    st.markdown(
        f"<a href='{url_whatsapp}' target='_blank'>"
        f"<button style='background-color:#25D366;color:white;padding:10px 15px;border:none;border-radius:5px;'>"
        "Enviar pedido por WhatsApp</button></a>",
        unsafe_allow_html=True
    )

# Cargar catálogo con IDs
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes_archivos = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes_archivos.sort()
catalogo = {}
tallas_disponibles = set()
patron = re.compile(r"- ([\d,()]+) -")

for i, archivo in enumerate(imagenes_archivos):
    nombre_archivo = os.path.splitext(archivo)[0]
    partes = nombre_archivo.split(" - ")
    if len(partes) != 3:
        continue

    referencia = partes[0].strip()
    tallas_info = partes[1].strip()
    precio = int(partes[2].strip())
    tallas = re.findall(r"(\d+)\((\d+)\)", tallas_info)

    producto_id = f"item_{i}"
    catalogo[producto_id] = {
        "id": producto_id,
        "archivo": archivo,
        "referencia": referencia,
        "precio": precio,
        "tallas": tallas
    }

    for t, _ in tallas:
        tallas_disponibles.add(t)

# Filtro por talla
tallas_ordenadas = sorted(tallas_disponibles, key=int)
talla_seleccionada_filtro = st.selectbox("Filtrar por talla", ["Todas"] + tallas_ordenadas)

# Mostrar catálogo
for producto_id, item in catalogo.items():
    referencia = item["referencia"]
    precio = item["precio"]
    archivo = item["archivo"]
    tallas = item["tallas"]

    if talla_seleccionada_filtro != "Todas":
        if not any(t == talla_seleccionada_filtro for t, _ in tallas):
            continue

    col1, col2 = st.columns([2, 3])
    with col1:
        st.image(os.path.join(carpeta, archivo), width=350)
    with col2:
        st.markdown(f"### {referencia}")
        st.markdown(f"<h4 style='color: green;'>${precio:,.0f}</h4>", unsafe_allow_html=True)

        cols_tallas = st.columns(len(tallas))
        for idx, (t, c) in enumerate(tallas):
            disabled = int(c) == 0
            with cols_tallas[idx]:
                if st.button(f"{t}", key=f"select_{producto_id}_{t}", disabled=disabled):
                    st.session_state.tallas_seleccionadas[producto_id] = t
                    clave = f"{producto_id}_{t}"
                    if clave not in st.session_state.carrito:
                        st.session_state.carrito[clave] = {
                            "referencia": referencia,
                            "precio": precio,
                            "talla": t,
                            "cantidad": 1
                        }

        # Mostrar controles de cantidad en columna separada
        st.markdown("#### Cantidad:")
        for t, _ in tallas:
            clave = f"{producto_id}_{t}"
            cantidad_actual = st.session_state.carrito.get(clave, {"cantidad": 0})["cantidad"]

            colm1, colm2, colm3 = st.columns([1, 1, 1])
            with colm1:
                if st.button("-", key=f"menos_{clave}"):
                    if cantidad_actual > 0:
                        st.session_state.carrito[clave]["cantidad"] -= 1
                        if st.session_state.carrito[clave]["cantidad"] <= 0:
                            del st.session_state.carrito[clave]
            with colm2:
                st.markdown(f"<div style='text-align:center;font-weight:bold;'>{cantidad_actual}</div>", unsafe_allow_html=True)
            with colm3:
                if st.button("+", key=f"mas_{clave}"):
                    if clave in st.session_state.carrito:
                        st.session_state.carrito[clave]["cantidad"] += 1
                    else:
                        st.session_state.carrito[clave] = {
                            "referencia": referencia,
                            "precio": precio,
                            "talla": t,
                            "cantidad": 1
                        }

    st.markdown("---")
