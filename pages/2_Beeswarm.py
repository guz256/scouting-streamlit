# -*- coding: utf-8 -*-
"""
Beeswarm Plot con jugador destacado - Diseño unificado con filtros globales
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.utils import load_data, filtros_sidebar

# Configurar diseño
st.set_page_config(layout="wide")

# Cargar datos y aplicar filtros generales
df = load_data()
df_filtrado = filtros_sidebar(df)

# Título
st.title("⚽ Comparación Percentilizada de Jugadores")
st.markdown("Visualización tipo beeswarm de métricas percentilizadas. Podés destacar uno o dos jugadores.")

# Métricas a graficar
metrics = [
    'Percentil Goles', 'Percentil xG', 'Percentil Remates',
    'Percentil Remates al Arco', 'Percentil Regates', 'Percentil Regates Exitosos',
    'Percentil Asistencias', 'Percentil xA', 'Percentil Jugadas Claves',
    'Percentil Toques en el Área', 'Percentil Duelos Defensivos',
    'Percentil Duelos Defensivos Ganados', 'Percentil Duelos Aereos',
    'Percentil Duelos Aereos Ganados', 'Percentil Entradas', 'Percentil Interceptaciones'
]

# Validar métricas disponibles
valid_metrics = [m for m in metrics if m in df_filtrado.columns]

# Convertir a formato largo
df_melted = df_filtrado.melt(
    id_vars=["Jugador", "Equipo", "Torneo", "Posición", "Minutos jugados"],
    value_vars=valid_metrics,
    var_name="Métrica", value_name="Valor"
)

# Verificación de datos
if df_melted.empty:
    st.warning("⚠️ No hay datos suficientes con los filtros aplicados.")
    st.stop()

# Seleccionar jugadores
jugadores = sorted(df_melted["Jugador"].dropna().unique())
jugador_destacado = st.selectbox("⭐ Jugador a destacar", jugadores)
jugador_destacado_2 = st.selectbox("⭐ Segundo jugador a destacar (opcional)", ["Ninguno"] + jugadores)

# Obtener info para título
info = df_melted[df_melted["Jugador"] == jugador_destacado].iloc[0]
torneo_sel = info["Torneo"]
posicion_sel = info["Posición"]

# Crear subgráficos
fig = make_subplots(
    rows=len(valid_metrics), cols=1, shared_xaxes=True,
    subplot_titles=[m.replace("Percentil ", "") for m in valid_metrics],
    vertical_spacing=0.02
)

# Dibujar cada métrica
for i, metrica in enumerate(valid_metrics, start=1):
    df_metric = df_melted[df_melted["Métrica"] == metrica].dropna()

    x_vals = df_metric["Valor"].values
    y_vals = np.zeros(len(x_vals))
    nombres = df_metric["Jugador"].values

    # Máscaras
    destacado_mask = nombres == jugador_destacado
    segundo_mask = nombres == jugador_destacado_2 if jugador_destacado_2 != "Ninguno" else np.array([False] * len(nombres))
    no_destacado_mask = ~(destacado_mask | segundo_mask)

    # Puntos no destacados
    fig.add_trace(
        go.Scatter(
            x=x_vals[no_destacado_mask],
            y=y_vals[no_destacado_mask],
            mode="markers",
            marker=dict(size=9, color="#D6DBDF", symbol="circle", opacity=0.2),
            text=nombres[no_destacado_mask],
            hovertemplate=f"<b>%{{text}}</b><br>{metrica}: %{{x}}<extra></extra>",
            showlegend=False
        ),
        row=i, col=1
    )

    # Jugador destacado
    if destacado_mask.any():
        fig.add_trace(
            go.Scatter(
                x=x_vals[destacado_mask],
                y=y_vals[destacado_mask],
                mode="markers",
                marker=dict(size=12, color="#0059b3", symbol="square", opacity=1.0),
                text=nombres[destacado_mask],
                hovertemplate=f"<b>%{{text}}</b><br>{metrica}: %{{x}}<extra></extra>",
                showlegend=False
            ),
            row=i, col=1
        )

    # Segundo jugador (opcional)
    if jugador_destacado_2 != "Ninguno" and (jugador_destacado_2 != jugador_destacado) and segundo_mask.any():
        fig.add_trace(
            go.Scatter(
                x=x_vals[segundo_mask],
                y=y_vals[segundo_mask],
                mode="markers",
                marker=dict(size=12, color="#cc3333", symbol="diamond", opacity=1.0),
                text=nombres[segundo_mask],
                hovertemplate=f"<b>%{{text}}</b><br>{metrica}: %{{x}}<extra></extra>",
                showlegend=False
            ),
            row=i, col=1
        )

    fig.update_yaxes(visible=False, row=i, col=1)
    fig.update_xaxes(visible=False, range=[0, 105], row=i, col=1)

# Definir título dinámico
title_text = f"<b>{jugador_destacado}</b>"
if jugador_destacado_2 != "Ninguno" and jugador_destacado_2 != jugador_destacado:
    title_text += f" vs <b>{jugador_destacado_2}</b>"

# Layout general
fig.update_layout(
    height=50 * len(valid_metrics),
    width=500,
    title={
        "text": f"{title_text}<br><span style='font-size:14px;'>Percentiles por métrica ({posicion_sel}, {torneo_sel})</span>",
        "x": 0.5, "xanchor": "center", "y": 0.98, "yanchor": "top"
    },
    template="simple_white",
    margin=dict(t=90, b=40, l=50, r=30),
    showlegend=False
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=False)

# Footer

from utils.footer import mostrar_footer

mostrar_footer()


