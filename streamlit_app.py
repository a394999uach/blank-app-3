import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import requests

st.set_page_config(page_title="El agua en México: Disponibilidad y Desperdicio💧", layout="centered")

st.markdown("<style>.main {background-color: #F4F8FB;} h1 {color: #1B4965; text-align: center;} h3 {color: #62B6CB;}</style>", unsafe_allow_html=True)

st.title("💧 El agua en México: disponibilidad, calidad y desperdicio")
st.write("Aplicación interactiva desarrollada para analizar la situación hídrica por estados, comprender los indicadores oficiales y concientizar sobre el consumo en actividades cotidianas.")

estados_mexico = [
    "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", "Chiapas",
    "Chihuahua", "Ciudad de México", "Coahuila", "Colima", "Durango", "Estado de México",
    "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Michoacán", "Morelos", "Nayarit",
    "Nuevo León", "Oaxaca", "Puebla", "Querétaro", "Quintana Roo", "San Luis Potosí",
    "Sinaloa", "Sonora", "Tabasco", "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
]
estados_mexico = sorted(list(set(estados_mexico)))

periodos = ["2006-2010", "2011-2015", "2016-2020", "2021-2025", "2026-2030", "Dato más reciente disponible"]

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
    "Quintana Roo": {"cobertura": 97.1, "potabilidad": "Aceptable (Monitoreo de dure
