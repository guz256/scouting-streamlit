# -*- coding: utf-8 -*-
"""
Updated: 2025-05-14
Radar Comparativo adaptado al diseño unificado
"""
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils.utils import load_data, filtros_sidebar
from utils.radar_utils import crear_radar, extraer_valores, aplicar_estilo_radar

# Layout general
st.set_page_config(layout="wide")

# Cargar y filtrar datos
df = load_data()
df_filtrado = filtros_sidebar(df)

# Título
st.title("🎯 Radar Comparativo")
st.markdown("Comparativa de métricas percentilizadas entre dos jugadores de la misma posición.")

# Diccionario de métricas por posición
metricas_por_posicion = {
    "Zaguero": [
        'Percentil Duelos Defensivos', 'Percentil Duelos Defensivos Ganados', 'Percentil Duelos Aereos',
        'Percentil Duelos Aereos Ganados', 'Percentil Interceptaciones', 'Percentil Entradas',
        'Percentil Carreras En Progresion', 'Percentil Aceleraciones',
        'Percentil Pases Progresivos', 'Percentil Pases Progresivos Acertados',
        'Percentil Pases', 'Percentil Pases Acertados', 'Percentil Pases Largos',
        'Percentil Pases Largos Acertados', 'Percentil Pases Al Ultimo Tercio',
        'Percentil Pases Al Ultimo Tercio Acertados'
    ],
    "Lateral": [
        'Percentil Duelos Defensivos', 'Percentil Duelos Defensivos Ganados', 'Percentil Duelos Aereos',
        'Percentil Duelos Aereos Ganados', 'Percentil Entradas', 'Percentil Interceptaciones', 
        'Percentil Carreras En Progresion', 'Percentil Regates', 'Percentil Duelos Ofensivos',
        'Percentil Centros', 'Percentil Centros Acertados', 'Percentil Pases Progresivos Acertados',
        'Percentil Pases Al Ultimo Tercio Acertados', 'Percentil Jugadas Claves', 'Percentil xA'
    ],
    "Interior": [
        'Percentil Goles', 'Percentil xG', 'Percentil Remates', 'Percentil Toques en el Área',
        'Percentil Asistencias', 'Percentil xA', 'Percentil Jugadas Claves',
        'Percentil Pases Acertados', 'Percentil Pases Hacia Adelante Acertados',
        'Percentil Carreras En Progresion', 'Percentil Duelos Defensivos', 'Percentil Duelos Defensivos Ganados',
        'Percentil Interceptaciones', 'Percentil Entradas'
    ],
    "Volante": [
        'Percentil Pases', 'Percentil Pases Acertados', 'Percentil Pases Progresivos', 'Percentil Pases Progresivos Acertados',
        'Percentil Pases Al Ultimo Tercio', 'Percentil Pases Al Ultimo Tercio Acertados',
        'Percentil Carreras En Progresion', 'Percentil xA', 'Percentil Asistencias', 'Percentil Jugadas Claves',
        'Percentil Duelos Defensivos', 'Percentil Duelos Defensivos Ganados', 'Percentil Entradas', 'Percentil Interceptaciones'
    ],
    "Mediapunta": [
        'Percentil Goles', 'Percentil xG', 'Percentil Remates', 'Percentil Remates al Arco', 'Percentil Asistencias',
        'Percentil xA', 'Percentil Jugadas Claves', 'Percentil Toques en el Área',
        'Percentil Pases Al Ultimo Tercio', 'Percentil Pases en Profundidad Acertados',
        'Percentil Pases Progresivos', 'Percentil Regates', 'Percentil Regates Exitosos'
    ],
    "Extremo": [
        'Percentil Goles', 'Percentil xG', 'Percentil Remates', 'Percentil Remates al Arco',
        'Percentil Regates', 'Percentil Regates Exitosos', 'Percentil Duelos Ofensivos', 'Percentil Toques en el Área',
        'Percentil Centros', 'Percentil Centros Acertados',
        'Percentil Asistencias', 'Percentil xA', 'Percentil Jugadas Claves'
    ],
    "Delantero": [
        'Percentil Goles', 'Percentil xG', 'Percentil Remates',
        'Percentil Remates al Arco', 'Percentil Conversión',
        'Percentil Asistencias', 'Percentil xA', 'Percentil Jugadas Claves',
        'Percentil Toques en el Área', 'Percentil Pases Progresivos',
        'Percentil Duelos Ofensivos', 'Percentil Regates'
    ]
}

# Posición seleccionada desde filtros generales
pos_seleccionada = df_filtrado["Posición"].iloc[0]

# Validar que la posición tenga radar definido
if pos_seleccionada not in metricas_por_posicion:
    st.warning(f"No hay configuración de radar definida para la posición: {pos_seleccionada}")
    st.stop()

columns_to_plot = metricas_por_posicion[pos_seleccionada]

# Filtrar DataFrame por posición específica
df_pos = df_filtrado[df_filtrado['Posición'].str.contains(pos_seleccionada, na=False)]

# Verificar que haya al menos dos jugadores disponibles
jugadores = df_pos['Jugador'].unique()
if len(jugadores) < 2:
    st.warning("⚠️ No hay suficientes jugadores para comparar en esta posición con los filtros aplicados.")
    st.stop()

# --- Layout para selección y gráfico ---
st.divider()
col1, col2 = st.columns([1, 5])

with col1:
    jug1 = st.selectbox("Jugador 1", jugadores)
    jug2 = st.selectbox("Jugador 2", jugadores, index=1 if len(jugadores) > 1 else 0)

with col2:
    row1_filt = df_pos[df_pos['Jugador'] == jug1]
    row2_filt = df_pos[df_pos['Jugador'] == jug2]

    if row1_filt.empty or row2_filt.empty:
        st.error("Uno de los jugadores seleccionados no tiene datos válidos en esta posición.")
        st.stop()

    val1 = extraer_valores(df_pos, jug1, columns_to_plot)
    val2 = extraer_valores(df_pos, jug2, columns_to_plot)

    radar = crear_radar(columns_to_plot)
    fig, ax = radar.setup_axis()
    radar.draw_circles(ax=ax, facecolor='#edf2f4', edgecolor='#fdc0c0', lw=1.5, zorder=1)
    radar.draw_radar_compare(
        ax=ax,
        values=val1,
        compare_values=val2,
        kwargs_radar={'facecolor': '#0059b3', 'alpha': 0.6},
        kwargs_compare={'facecolor': '#cc3333', 'alpha': 0.6}
    )
    radar.draw_range_labels(ax=ax, fontsize=11, fontproperties="monospace", color='#6C969D')
    radar.draw_param_labels(ax=ax, fontsize=10, fontproperties="monospace", color='#003366')

    row1 = row1_filt.iloc[0]
    row2 = row2_filt.iloc[0]
    label1 = f"{jug1}\n{row1['Edad']} años\n{row1['Torneo']} - {row1['Equipo']}"
    label2 = f"{jug2}\n{row2['Edad']} años\n{row2['Torneo']} - {row2['Equipo']}"
    aplicar_estilo_radar(ax, label1, label2)

    fig.set_size_inches(9, 9)  # Cambiá a (4, 4) o (6, 6) si querés probar otros tamaños
    st.pyplot(fig)

# Footer
from utils.footer import mostrar_footer

mostrar_footer()