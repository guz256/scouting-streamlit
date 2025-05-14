# -*- coding: utf-8 -*-
"""
Scatter Comparativo - Diseño unificado con líneas promedio y jugadores destacados
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.utils import load_data, filtros_sidebar

# Configurar diseño
st.set_page_config(layout="wide")

# Cargar datos y aplicar filtros generales
df = load_data()
df_filtrado = filtros_sidebar(df)

# Título
st.title("📊 Comparativa entre Métricas")
st.markdown("Visualización de dispersión entre dos métricas numéricas, con opción de destacar uno o dos jugadores y líneas promedio.")

# Columnas numéricas disponibles
numeric_cols = df_filtrado.select_dtypes(include="number").columns.tolist()

# Layout para seleccionar métricas y jugadores
st.divider()
col1, col2 = st.columns(2)

with col1:
    x_metric = st.selectbox("📈 Eje X", numeric_cols)
with col2:
    y_metric = st.selectbox("📉 Eje Y", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)

# Jugadores a destacar
jugadores = sorted(df_filtrado["Jugador"].dropna().unique())
destacado_1 = st.selectbox("⭐ Jugador a destacar", jugadores)
destacado_2 = st.selectbox("⭐ Segundo jugador a destacar (opcional)", ["Ninguno"] + jugadores)

# Agregar columnas para color y símbolo
df_filtrado["Color"] = "#a6d5fa"     # default
df_filtrado["Símbolo"] = "circle"   # default

df_filtrado.loc[df_filtrado["Jugador"] == destacado_1, "Color"] = "#0059b3"
df_filtrado.loc[df_filtrado["Jugador"] == destacado_1, "Símbolo"] = "square"

if destacado_2 != "Ninguno" and destacado_2 != destacado_1:
    df_filtrado.loc[df_filtrado["Jugador"] == destacado_2, "Color"] = "#cc3333"
    df_filtrado.loc[df_filtrado["Jugador"] == destacado_2, "Símbolo"] = "diamond"

# Crear figura con plotly.graph_objects
fig = go.Figure()

for simbolo in df_filtrado["Símbolo"].unique():
    subset = df_filtrado[df_filtrado["Símbolo"] == simbolo]
    custom_data = subset[["Equipo", "Edad"]].values

    fig.add_trace(go.Scatter(
        x=subset[x_metric],
        y=subset[y_metric],
        mode="markers",
        marker=dict(
            color=subset["Color"],
            symbol=subset["Símbolo"],
            size=10,
            line=dict(width=0.5, color='DarkSlateGrey')
        ),
        text=subset["Jugador"],
        customdata=custom_data,
        hovertemplate=(
            "<b>%{text}</b><br>"
            f"{x_metric}: %{{x}}<br>"
            f"{y_metric}: %{{y}}<br>"
            "Equipo: %{customdata[0]}<br>"
            "Edad: %{customdata[1]}<extra></extra>"
        ),
        name=f"{simbolo}"
    ))

# Líneas promedio
x_avg = df_filtrado[x_metric].mean()
y_avg = df_filtrado[y_metric].mean()

fig.add_shape(
    type="line",
    x0=x_avg, x1=x_avg,
    y0=df_filtrado[y_metric].min(), y1=df_filtrado[y_metric].max(),
    line=dict(color="gray", width=1.5, dash="dash"),
)

fig.add_shape(
    type="line",
    x0=df_filtrado[x_metric].min(), x1=df_filtrado[x_metric].max(),
    y0=y_avg, y1=y_avg,
    line=dict(color="gray", width=1.5, dash="dash"),
)

# Layout final
fig.update_layout(
    xaxis_title=x_metric,
    yaxis_title=y_metric,
    template="simple_white",
    height=600,
    margin=dict(l=40, r=40, t=40, b=40),
    showlegend=False
)

# Mostrar gráfico
st.plotly_chart(fig, use_container_width=True)

# Footer
from utils.footer import mostrar_footer

mostrar_footer()
