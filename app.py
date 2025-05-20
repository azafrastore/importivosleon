import streamlit as st
import os
import re

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

    
carpeta = "catalogo"
extensiones_validas = (".png", ".jpg", ".jpeg", ".webp", ".jfif")
imagenes = [f for f in os.listdir(carpeta) if f.lower().endswith(extensiones_validas)]
imagenes.sort()


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
talla_seleccionada = st.selectbox("Filtrar por talla", ["Todas"] + tallas_ordenadas)


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

        # Obtener tallas y cantidades como lista de tuplas (talla, cantidad)
        tallas = re.findall(r"(\d+)\((\d+)\)", tallas_info)
        if talla_seleccionada != "Todas":
            if not any(talla_seleccionada == t for t, _ in tallas):
                continue  # No mostrar si la talla no está

        # Crear columnas para imagen, referencia y precio/botón
        col1, col2, col3 = st.columns([2, 3, 2])

        with col1:
            st.image(os.path.join(carpeta, archivo), use_container_width=True)

        with col2:
            st.markdown(f"### {referencia}")
          #  for talla, cantidad in tallas:
           #     plural = "pares" if int(cantidad) > 1 else "par"
            #    st.markdown(f"- Talla {talla}: {cantidad} {plural}")

        with col3:
            st.markdown(f"<h4 style='color: green;'>${precio_formateado}</h4>", unsafe_allow_html=True)

            for t, c in tallas:
                clave = f"{archivo}_{t}"
                cantidad_actual = st.session_state.carrito.get(clave, {"cantidad": 0})["cantidad"]

                col_minus, col_plus, col_info = st.columns([1, 1, 3])
                with col_minus:
                    if st.button("-1", key=f"menos_{archivo}_{t}"):
                        if cantidad_actual > 0:
                            if clave in st.session_state.carrito:
                                st.session_state.carrito[clave]["cantidad"] -= 1
                                if st.session_state.carrito[clave]["cantidad"] <= 0:
                                    del st.session_state.carrito[clave]

                with col_plus:
                    if st.button("+1", key=f"mas_{archivo}_{t}"):
                        if clave in st.session_state.carrito:
                            st.session_state.carrito[clave]["cantidad"] += 1
                        else:
                            st.session_state.carrito[clave] = {
                                "referencia": referencia,
                                "precio": precio,
                                "talla": t,
                                "cantidad": 1
                            }

                with col_info:
                    plural = "pares" if int(c) > 1 else "par"
                    #    st.markdown(f"- Talla {talla}: {cantidad} {plural}")
                    st.write(f"Talla {t}: {c} {plural}| En carrito: {cantidad_actual}")

        st.markdown("---")
    except Exception as e:
        st.warning(f"Error con archivo '{archivo}': {e}")


