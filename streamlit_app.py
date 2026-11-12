import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(
    page_title="El agua en México: Disponibilidad y Desperdicio",
    layout="centered"
)

st.markdown(
    "<style>.main {background-color: #F4F8FB;} "
    "h1 {color: #1B4965; text-align: center;} "
    "h3 {color: #62B6CB;}</style>",
    unsafe_allow_html=True
)

st.title("💧 El agua en México: disponibilidad, calidad y desperdicio")
st.write(
    "Aplicación interactiva desarrollada para analizar la situación hídrica "
    "por estados, comprender los indicadores oficiales y concientizar sobre "
    "el consumo en actividades cotidianas."
)

estados_mexico = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche",
    "Chiapas", "Chihuahua", "Ciudad de México", "Coahuila", "Colima",
    "Durango", "Estado de México", "Guanajuato", "Guerrero", "Hidalgo",
    "Jalisco", "Michoacán", "Morelos", "Nayarit", "Nuevo León", "Oaxaca",
    "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí", "Sinaloa",
    "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán",
    "Zacatecas"
]
estados_mexico = sorted(list(set(estados_mexico)))

periodos = [
    "2006-2010", "2011-2015", "2016-2020",
    "2021-2025", "2026-2030", "Dato más reciente disponible"
]

datos_disponibilidad = {
    "Aguascalientes": {"2006-2010": 420, "2011-2015": 390, "2016-2020": 360, "2021-2025": 340, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 340},
    "Baja California": {"2006-2010": 980, "2011-2015": 920, "2016-2020": 870, "2021-2025": 810, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 810},
    "Baja California Sur": {"2006-2010": 780, "2011-2015": 730, "2016-2020": 690, "2021-2025": 650, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 650},
    "Campeche": {"2006-2010": 18500, "2011-2015": 18000, "2016-2020": 17500, "2021-2025": 16900, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 16900},
    "Chiapas": {"2006-2010": 24000, "2011-2015": 23200, "2016-2020": 22500, "2021-2025": 21800, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 21800},
    "Chihuahua": {"2006-2010": 1850, "2011-2015": 1720, "2016-2020": 1610, "2021-2025": 1540, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1540},
    "Ciudad de México": {"2006-2010": 160, "2011-2015": 150, "2016-2020": 140, "2021-2025": 130, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 130},
    "Coahuila": {"2006-2010": 1450, "2011-2015": 1380, "2016-2020": 1310, "2021-2025": 1250, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1250},
    "Colima": {"2006-2010": 3200, "2011-2015": 3050, "2016-2020": 2900, "2021-2025": 2780, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 2780},
    "Durango": {"2006-2010": 3100, "2011-2015": 2950, "2016-2020": 2800, "2021-2025": 2680, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 2680},
    "Estado de México": {"2006-2010": 260, "2011-2015": 240, "2016-2020": 220, "2021-2025": 210, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 210},
    "Guanajuato": {"2006-2010": 680, "2011-2015": 630, "2016-2020": 590, "2021-2025": 550, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 550},
    "Guerrero": {"2006-2010": 5800, "2011-2015": 5500, "2016-2020": 5200, "2021-2025": 4950, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 4950},
    "Hidalgo": {"2006-2010": 1950, "2011-2015": 1850, "2016-2020": 1750, "2021-2025": 1680, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1680},
    "Jalisco": {"2006-2010": 1550, "2011-2015": 1470, "2016-2020": 1390, "2021-2025": 1320, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1320},
    "Michoacán": {"2006-2010": 2900, "2011-2015": 2750, "2016-2020": 2600, "2021-2025": 2480, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 2480},
    "Morelos": {"2006-2010": 1150, "2011-2015": 1080, "2016-2020": 1020, "2021-2025": 970, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 970},
    "Nayarit": {"2006-2010": 7800, "2011-2015": 7400, "2016-2020": 7000, "2021-2025": 6650, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 6650},
    "Nuevo León": {"2006-2010": 1300, "2011-2015": 1200, "2016-2020": 1100, "2021-2025": 1020, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1020},
    "Oaxaca": {"2006-2010": 8500, "2011-2015": 8100, "2016-2020": 7700, "2021-2025": 7300, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 7300},
    "Puebla": {"2006-2010": 950, "2011-2015": 890, "2016-2020": 840, "2021-2025": 790, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 790},
    "Querétaro": {"2006-2010": 820, "2011-2015": 770, "2016-2020": 720, "2021-2025": 680, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 680},
    "Quintana Roo": {"2006-2010": 12500, "2011-2015": 11800, "2016-2020": 11100, "2021-2025": 10500, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 10500},
    "San Luis Potosí": {"2006-2010": 1650, "2011-2015": 1560, "2016-2020": 1480, "2021-2025": 1400, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1400},
    "Sinaloa": {"2006-2010": 5200, "2011-2015": 4900, "2016-2020": 4600, "2021-2025": 4350, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 4350},
    "Sonora": {"2006-2010": 2800, "2011-2015": 2650, "2016-2020": 2500, "2021-2025": 2380, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 2380},
    "Tabasco": {"2006-2010": 22000, "2011-2015": 21500, "2016-2020": 20800, "2021-2025": 19900, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 19900},
    "Tamaulipas": {"2006-2010": 2100, "2011-2015": 1980, "2016-2020": 1870, "2021-2025": 1780, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1780},
    "Tlaxcala": {"2006-2010": 510, "2011-2015": 480, "2016-2020": 450, "2021-2025": 420, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 420},
    "Veracruz": {"2006-2010": 11500, "2011-2015": 10900, "2016-2020": 10300, "2021-2025": 9800, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 9800},
    "Yucatán": {"2006-2010": 9200, "2011-2015": 8700, "2016-2020": 8200, "2021-2025": 7800, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 7800},
    "Zacatecas": {"2006-2010": 1250, "2011-2015": 1180, "2016-2020": 1110, "2021-2025": 1050, "2026-2030": "Sin datos disponibles", "Dato más reciente disponible": 1050}
}

datos_cobertura_potable = {
    "Aguascalientes": {"cobertura": 98.8, "potabilidad": "Buena (Tratamiento constante)"},
    "Baja California": {"cobertura": 97.5, "potabilidad": "Aceptable / Alta salinidad en zonas"},
    "Baja California Sur": {"cobertura": 95.2, "potabilidad": "Moderada (Presencia de minerales)"},
    "Campeche": {"cobertura": 89.4, "potabilidad": "Aceptable"},
    "Chiapas": {"cobertura": 88.8, "potabilidad": "Baja en zonas rurales (Riesgo biológico)"},
    "Chihuahua": {"cobertura": 98.1, "potabilidad": "Buena (Monitoreo continuo de arsénico)"},
    "Ciudad de México": {"cobertura": 98.6, "potabilidad": "Variable según alcaldía / Red antigua"},
    "Coahuila": {"cobertura": 98.4, "potabilidad": "Aceptable"},
    "Colima": {"cobertura": 99.0, "potabilidad": "Buena"},
    "Durango": {"cobertura": 96.5, "potabilidad": "Moderada (Presencia de flúor en acuíferos)"},
    "Estado de México": {"cobertura": 96.2, "potabilidad": "Variable / Presión intermitente"},
    "Guanajuato": {"cobertura": 96.8, "potabilidad": "Moderada (Tratamiento por metales en pozos)"},
    "Guerrero": {"cobertura": 87.1, "potabilidad": "Baja (Deficiencia en cloración municipal)"},
    "Hidalgo": {"cobertura": 94.3, "potabilidad": "Aceptable"},
    "Jalisco": {"cobertura": 97.8, "potabilidad": "Buena en ZMM / Variable en zonas agrícolas"},
    "Michoacán": {"cobertura": 94.6, "potabilidad": "Aceptable"},
    "Morelos": {"cobertura": 96.9, "potabilidad": "Buena"},
    "Nayarit": {"cobertura": 95.1, "potabilidad": "Aceptable"},
    "Nuevo León": {"cobertura": 98.9, "potabilidad": "Alta (Red automatizada y potabilizada)"},
    "Oaxaca": {"cobertura": 85.5, "potabilidad": "Baja en zonas rurales (Falta de potabilizadoras)"},
    "Puebla": {"cobertura": 94.8, "potabilidad": "Aceptable / Vulnerable en cuencas urbanas"},
    "Querétaro": {"cobertura": 97.3, "potabilidad": "Buena"},
    "Quintana Roo": {"cobertura": 97.1, "potabilidad": "Aceptable (Monitoreo de dureza y karst)"},
    "San Luis Potosí": {"cobertura": 94.2, "potabilidad": "Moderada"},
    "Sinaloa": {"cobertura": 96.7, "potabilidad": "Aceptable"},
    "Sonora": {"cobertura": 97.6, "potabilidad": "Moderada (Tratamiento en acuíferos del norte)"},
    "Tabasco": {"cobertura": 88.2, "potabilidad": "Moderada (Alta turbiedad en ríos)"},
    "Tamaulipas": {"cobertura": 96.1, "potabilidad": "Aceptable"},
    "Tlaxcala": {"cobertura": 97.9, "potabilidad": "Aceptable"},
    "Veracruz": {"cobertura": 89.7, "potabilidad": "Variable (Vulnerable a eventos meteorológicos)"},
    "Yucatán": {"cobertura": 96.8, "potabilidad": "Moderada (Agua dura / Acuífero somero)"},
    "Zacatecas": {"cobertura": 96.3, "potabilidad": "Moderada"}
}

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

st.subheader("1. Consulta por Estado y Periodo")

col1, col2 = st.columns(2)

with col1:
    default_index = estados_mexico.index("Chihuahua") if "Chihuahua" in estados_mexico else 0
    estado_seleccionado = st.selectbox(
        "Selecciona un estado de México:",
        estados_mexico,
        index=default_index
    )

with col2:
    periodo_seleccionado = st.selectbox(
        "Selecciona el periodo:",
        periodos,
        index=3
    )

st.subheader("2. Indicadores Hídricos y Potabilidad")

disp_valor = "Sin datos disponibles"
if estado_seleccionado in datos_disponibilidad:
    if periodo_seleccionado in datos_disponibilidad[estado_seleccionado]:
        disp_valor = datos_disponibilidad[estado_seleccionado][periodo_seleccionado]

info_cobertura = datos_cobertura_potable.get(
    estado_seleccionado,
    {"cobertura": "N/D", "potabilidad": "Sin datos"}
)

col_m1, col_m2, col_m3 = st.columns(3)

with col_m1:
    if isinstance(disp_valor, (int, float)):
        st.metric(
            label=f"Disponibilidad per Cápita ({periodo_seleccionado})",
            value=f"{disp_valor:,.0f} m³/hab/año"
        )
    else:
        st.metric(
            label=f"Disponibilidad per Cápita ({periodo_seleccionado})",
            value=disp_valor
        )

with col_m2:
    st.metric(
        label="Cobertura de Agua Entubada",
        value=f"{info_cobertura['cobertura']}%"
    )

with col_m3:
    st.metric(
        label="Calidad / Potabilidad General",
        value=info_cobertura["potabilidad"]
    )

st.info(
    "💡 **¿Qué significan estos indicadores?**\n"
    "- **Disponibilidad:** Mide el agua renovable total del estado dividida entre su población.\n"
    "- **Cobertura:** Porcentaje de hogares conectados a la red pública de agua entubada (Fuente: INEGI).\n"
    "- **Potabilidad:** Diagnóstico regional sobre la aptitud del agua para uso doméstico."
)

# ==========================================
# SECCIÓN: Mapa de Consumo por Estado (Altair)
# ==========================================
st.markdown("---")
st.subheader("🗺️ Mapa de Consumo Total de Agua por Estado")
st.write(
    "Visualización geográfica del volumen anual de agua concesionada/consumida "
    "(incluye uso agrícola, público e industrial en millones de m³)."
)

df_mapa = pd.DataFrame({
    "Estado": list(datos_consumo_agua.keys()),
    "Consumo_Mm3": list(datos_consumo_agua.values())
})

url_geojson = "https://raw.githubusercontent.com/angelnmara/geojson/master/mexicoHigh.json"
mapa_mexico = alt.Data(
    url=url_geojson,
    format=alt.DataFormat(property="features", type="json")
)

fig_mapa = alt.Chart(mapa_mexico).mark_geoshape(
    stroke="white",
    strokeWidth=0.8
).encode(
    color=alt.Color(
        "Consumo_Mm3:Q",
        scale=alt.Scale(scheme="blues"),
        title="Consumo (Mm³/año)"
    ),
    tooltip=[
        alt.Tooltip("properties.name:N", title="Estado"),
        alt.Tooltip("Consumo_Mm3:Q", title="Consumo (Mm³/año)", format=",.0f")
    ]
).transform_lookup(
    lookup="properties.name",
    from_=alt.LookupData(df_mapa, "Estado", ["Consumo_Mm3"])
).project(
    type="mercator"
).properties(
    width=650,
    height=420
)

st.altair_chart(fig_mapa, width="stretch")

estado_max = df_mapa.loc[df_mapa["Consumo_Mm3"].idxmax()]
consumo_sel = datos_consumo_agua.get(estado_seleccionado, 0)
st.warning(
    f"📊 **Mayor consumidor a nivel nacional:** **{estado_max['Estado']}** con aproximadamente "
    f"**{estado_max['Consumo_Mm3']:,.0f} millones de m³ al año** (impulsado principalmente por su alta actividad agrícola).\n\n"
    f"📍 **Estado seleccionado ({estado_seleccionado}):** Consume aproximadamente **{consumo_sel:,.0f} millones de m³ al año**."
)

st.markdown("---")

st.subheader("3. Simulador de desperdicio en botellas de agua (500 ml)")
st.write(
    "Calcula cuántas **botellas de 500 ml** y cuánto dinero tirarías a la basura "
    "si compraras esa misma cantidad de agua embotellada mientras esperas a que salga la caliente en la regadera."
)

col_s1, col_s2, col_s3, col_s4 = st.columns(4)

with col_s1:
    minutos_espera = st.slider("Minutos de espera:", 0, 10, 3)

with col_s2:
    caudal_regadera = st.slider("Caudal (Litros/min):", 2, 15, 8)

with col_s3:
    frecuencia_semanal = st.slider("Duchas por semana:", 1, 14, 7)

with col_s4:
    costo_botella = st.number_input("Precio por botella de 500ml (\$ MXN):", value=15.0, step=1.0)

litros_ducha = minutos_espera * caudal_regadera
litros_semana = litros_ducha * frecuencia_semanal
litros_mes = litros_semana * 4.33
litros_anio = litros_semana * 52

botellas_ducha = litros_ducha * 2
botellas_semana = litros_semana * 2
botellas_mes = litros_mes * 2
botellas_anio = litros_anio * 2

costo_ducha = botellas_ducha * costo_botella
costo_semana = botellas_semana * costo_botella
costo_mes = botellas_mes * costo_botella
costo_anio = botellas_anio * costo_botella

st.write("### 🫗 Impacto económico y volumen desperdiciado:")

res_col1, res_col2, res_col3, res_col4 = st.columns(4)

with res_col1:
    st.metric("Por ducha", f"\${costo_ducha:,.2f} MXN", f"{int(botellas_ducha):,} botellas")

with res_col2:
    st.metric("Por semana", f"\${costo_semana:,.2f} MXN", f"{int(botellas_semana):,} botellas")

with res_col3:
    st.metric("Por mes", f"\${costo_mes:,.2f} MXN", f"{int(botellas_mes):,} botellas")

with res_col4:
    st.metric("Por año", f"\${costo_anio:,.2f} MXN", f"{int(botellas_anio):,} botellas")

if botellas_anio > 0:
    df_grafica = pd.DataFrame({
        "Periodo": ["Por ducha", "Por semana", "Por mes", "Por año"],
        "Costo_MXN": [costo_ducha, costo_semana, costo_mes, costo_anio],
        "Botellas": [botellas_ducha, botellas_semana, botellas_mes, botellas_anio]
    })

    chart = alt.Chart(df_grafica).mark_bar(color="#62B6CB").encode(
        x=alt.X(
            "Periodo:N",
            sort=["Por ducha", "Por semana", "Por mes", "Por año"],
            title=None,
            axis=alt.Axis(labelAngle=0)
        ),
        y=alt.Y("Costo_MXN:Q", title="Dinero equivalente (\$ MXN)"),
        tooltip=[
            alt.Tooltip("Periodo:N", title="Periodo"),
            alt.Tooltip("Costo_MXN:Q", title="Costo Estimado ($ MXN)", format="$,.2f"),
            alt.Tooltip("Botellas:Q", title="Botellas (500 ml)", format=",.0f")
        ]
    )
