import streamlit as st
import os
import re
import urllib.parse

st.set_page_config(page_title="Importivos León", layout="wide")

# Inicializar carrito en la sesión
if "carrito" not in st.session_state:
    st.session_state.carrito = {}

# Encabezado con logo y título
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=150)
with col2:
    st.title("Nuestro Catálogo Deportivo")

# Dirección del local
st.markdown("<p style='font-size:16px; color: gray;'>Bucaramanga</p>", unsafe_allow_html=True)

# Carrito de compras
st.markdown("## 🛒 Carrito de compras")
if st.session_state.carrito:
    total = 0
    for key, item in st.session_state.carrito.items():
        subtotal = item["precio"] * item["cantidad"]
        total += subtotal
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.markdown(f"**{item['referencia']}**")
        with col2:
            st.markdown(f"{item['cantidad']} unidad(es)")
        with col3:
            st.markdown(f"${subtotal:,.0f}".replace(",", "."))

    st.success(f"**Total a pagar:** ${total:,.0f}".replace(",", "."))
    if st.button("🧹 Vaciar carrito"):
        st.session_state.carrito.clear()
else:
    st.info("Tu carrito está vacío.")

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
        f"<a href='{url_whatsapp}' target='_blank'><button style='background-color:#25D366;color:white;padding:10px 15px;border:none;border-radius:5px;'>Enviar pedido por WhatsApp</button></a>",
        unsafe_allow_html=True
    )

# Cargar imágenes del catálogo
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

# Detectar todas las tallas disponibles para el filtro
tallas_disponibles = set()
patron = re.compile(r"- ([\d,() ]+) -")
for archivo in imagenes:
    nombre_archivo = os.path.splitext(archivo)[0]
    coincidencia = patron.search(nombre_archivo)
    if coincidencia:
        tallas_info = coincidencia.group(1)
        tallas = re.findall(r"(\d+)\\((\d+)\\)", tallas_info)
        for t, _ in tallas:
            tallas_disponibles.add(t)

tallas_ordenadas = sorted(tallas_disponibles, key=int)
talla_seleccionada = st.selectbox("Filtrar por talla", ["Todas"] + tallas_ordenadas)

# Mostrar catálogo
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        partes = nombre_archivo.split(" - ")
        if len(partes) != 3:
            st.warning(f"Formato inválido en el archivo: {archivo}")
            continue

        referencia = partes[0].strip()
        tallas_info = partes[1].strip()
        precio = int(partes[2].strip())
        precio_formateado = "{:,.0f}".format(precio).replace(",", ".")

        tallas = re.findall(r"(\d+)\\((\d+)\\)", tallas_info)
        if talla_seleccionada != "Todas":
            if not any(talla_seleccionada == t for t, _ in tallas):
                continue

        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(os.path.join(carpeta, archivo), width=300)

        with col2:
            st.markdown(f"### {referencia}")
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

            st.markdown("<b>Tallas disponibles:</b>", unsafe_allow_html=True)
            talla_cols = st.columns(len(tallas))
            for i, (t, c) in enumerate(tallas):
                if int(c) > 0:
                    with talla_cols[i]:
                        if st.button(f"{t}", key=f"talla_{archivo}_{t}", help=f"Agregar talla {t}"):
                            clave = f"{archivo}_{t}"
                            if clave in st.session_state.carrito:
                                st.session_state.carrito[clave]["cantidad"] += 1
                            else:
                                st.session_state.carrito[clave] = {
                                    "referencia": referencia,
                                    "precio": precio,
                                    "talla": t,
                                    "cantidad": 1
                                }

            for t, c in tallas:
                clave = f"{archivo}_{t}"
                if clave in st.session_state.carrito:
                    cantidad_actual = st.session_state.carrito[clave]["cantidad"]
                    st.markdown(f"<b>Talla {t}</b>", unsafe_allow_html=True)
                    minus_col, num_col, plus_col = st.columns([1, 1, 1])
                    with minus_col:
                        if st.button("−", key=f"menos_{archivo}_{t}"):
                            if cantidad_actual > 1:
                                st.session_state.carrito[clave]["cantidad"] -= 1
                            else:
                                del st.session_state.carrito[clave]
                    with num_col:
                        st.markdown(f"<div style='text-align:center; font-size: 20px;'>{cantidad_actual}</div>", unsafe_allow_html=True)
                    with plus_col:
                        if st.button("+", key=f"mas_{archivo}_{t}"):
                            st.session_state.carrito[clave]["cantidad"] += 1

        st.markdown("---")
    except Exception as e:
        st.warning(f"Error con archivo '{archivo}': {e}")
