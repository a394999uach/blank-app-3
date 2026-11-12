!pip install streamlit plotly requests
import plotly.express as px
import requests

# ==========================================
# NUEVA SECCIÓN: Mapa de Consumo por Estado
# ==========================================
st.markdown("---")
st.subheader("🗺️ Mapa de Consumo Total de Agua por Estado")
st.write("Visualización geográfica del volumen anual de agua concesionada/consumida (incluye uso agrícola, público e industrial en millones de m³).")

# Datos aproximados de consumo/extracción anual por estado (Millones de m³ - Ref. CONAGUA)
datos_consumo_agua = {
    "Aguascalientes": 680, "Baja California": 2950, "Baja California Sur": 480,
    "Campeche": 510, "Chiapas": 2400, "Chihuahua": 5150,
    "Ciudad de México": 1150, "Coahuila": 2350, "Colima": 1520,
    "Durango": 2100, "Estado de México": 2450, "Guanajuato": 4450,
    "Guerrero": 1350, "Hidalgo": 2650, "Jalisco": 4850,
    "Michoacán": 5400, "Morelos": 1320, "Nayarit": 1680,
    "Nuevo León": 2150, "Oaxaca": 1580, "Puebla": 2250,
    "Querétaro": 1050, "Quintana Roo": 790, "San Luis Potosí": 1540,
    "Sinaloa": 9850, "Sonora": 7200, "Tabasco": 690,
    "Tamaulipas": 4300, "Tlaxcala": 360, "Veracruz": 5600,
    "Yucatán": 1480, "Zacatecas": 1750
}

# Función con caché para descargar el mapa GeoJSON de México una sola vez
@st.cache_data
def cargar_geojson_mexico():
    url = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
    response = requests.get(url)
    return response.json()

try:
    geojson_mexico = cargar_geojson_mexico()

    # Preparar DataFrame para el mapa
    df_mapa = pd.DataFrame({
        "Estado": list(datos_consumo_agua.keys()),
        "Consumo_Mm3": list(datos_consumo_agua.values())
    })

    # Crear mapa coroplético interactivo
    fig_mapa = px.choropleth(
        df_mapa,
        geojson=geojson_mexico,
        locations="Estado",
        featureidkey="properties.name", # Llave estándar en este GeoJSON para los nombres de estados
        color="Consumo_Mm3",
        color_continuous_scale="YlGnBu", # Escala de amarillo a azul oscuro
        labels={"Consumo_Mm3": "Consumo (Mm³/año)"},
        hover_name="Estado",
        hover_data={"Estado": False, "Consumo_Mm3": ":,.0f"}
    )

    # Enfocar la cámara exclusivamente en México y ocultar el resto del mundo
    fig_mapa.update_geos(
        fitbounds="locations",
        visible=False
    )
    fig_mapa.update_layout(
        margin={"r": 0, "t": 10, "l": 0, "b": 0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_mapa, use_container_width=True)

    # Destacar automáticamente el estado con mayor gasto
    estado_max = df_mapa.loc[df_mapa["Consumo_Mm3"].idxmax()]
    st.warning(f"📊 **Mayor consumidor a nivel nacional:** **{estado_max['Estado']}** con aproximadamente **{estado_max['Consumo_Mm3']:,.0f} millones de m³ al año** (impulsado principalmente por su alta actividad agrícola).")

except Exception as e:
    st.error(f"No se pudo cargar el mapa interactivo. Verifica tu conexión a internet. Detalle: {e}")
