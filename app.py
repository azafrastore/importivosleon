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

# Dirección
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
    if st.button("🧹 Vaciar carrito"):
        st.session_state.carrito.clear()
else:
    st.info("Tu carrito está vacío.")

# Botón para enviar pedido por WhatsApp
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

# Cargar catálogo
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()

# Filtrar tallas disponibles
tallas_disponibles = set()
patron = re.compile(r"- ([\d,()]+) -")
for archivo in imagenes:
    nombre_archivo = os.path.splitext(archivo)[0]
    coincidencia = patron.search(nombre_archivo)
    if coincidencia:
        tallas_info = coincidencia.group(1)
        tallas = re.findall(r"\d+", tallas_info)
        tallas_disponibles.update(tallas)

tallas_ordenadas = sorted(tallas_disponibles, key=int)
talla_filtro = st.selectbox("Filtrar por talla", ["Todas"] + tallas_ordenadas)

# Mostrar catálogo
for archivo in imagenes:
    try:
        nombre_archivo = os.path.splitext(archivo)[0]
        partes = nombre_archivo.split(" - ")
        if len(partes) != 3:
            continue

        referencia = partes[0].strip()
        tallas_info = partes[1].strip()
        precio = int(partes[2].strip())
        precio_formateado = "{:,.0f}".format(precio).replace(",", ".")

        tallas = re.findall(r"(\d+)\((\d+)\)", tallas_info)
        if talla_filtro != "Todas":
            if not any(talla_filtro == t for t, _ in tallas):
                continue

        # Sección visual
        col_img, col_info, col_qty = st.columns([2, 3, 1])
        with col_img:
            st.image(os.path.join(carpeta, archivo), width=350)

        with col_info:
            st.markdown(f"### {referencia}")
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

            tallas_disponibles = {t: int(c) for t, c in tallas}
            seleccionada = st.radio(
                f"Talla para {referencia}",
                options=list(tallas_disponibles.keys()),
                key=f"tallas_{archivo}",
                horizontal=True,
                index=0 if tallas_disponibles else None,
            )

        # Mostrar controles de cantidad
        clave = f"{archivo}_{seleccionada}"
        cantidad_actual = st.session_state.carrito.get(clave, {"cantidad": 0})["cantidad"]

        with col_qty:
            col_m, col_c, col_p = st.columns([1, 1, 1])
            with col_m:
                if st.button("−", key=f"menos_{clave}"):
                    if clave in st.session_state.carrito:
                        st.session_state.carrito[clave]["cantidad"] -= 1
                        if st.session_state.carrito[clave]["cantidad"] <= 0:
                            del st.session_state.carrito[clave]
            with col_c:
                st.markdown(f"<div style='text-align:center; font-weight:bold;'>{cantidad_actual}</div>", unsafe_allow_html=True)
            with col_p:
                if st.button("+", key=f"mas_{clave}"):
                    if clave in st.session_state.carrito:
                        st.session_state.carrito[clave]["cantidad"] += 1
                    else:
                        st.session_state.carrito[clave] = {
                            "referencia": referencia,
                            "precio": precio,
                            "talla": seleccionada,
                            "cantidad": 1
                        }

        st.markdown("---")
    except Exception as e:
        st.warning(f"Error con archivo '{archivo}': {e}")
