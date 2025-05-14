# -*- coding: utf-8 -*-
"""
Created on Mon May 12 14:27:26 2025

@author: guz_m
"""

import streamlit as st

st.set_page_config(page_title="Aplicación de Scouting", layout="wide")

st.title("📊 Aplicación de Scouting")
st.markdown("""
Bienvenid@ a la herramienta de análisis de rendimiento y scouting de jugadores.  
Esta aplicación te permite explorar distintos perfiles a través de métricas percentilizadas y visualizaciones interactivas.

Los datos son de Wyscout y corresponden a la Temporada 2024 de los siguientes torneos:
            Argentina Segunda División
            Argentina Federal A
            Chile Primera División
            Chile Segunda División
            Uruguay Primera División
            Uruguay Segunda División
       
*Los percentiles fueron cálculados por posición y por torneo.            

### ¿Qué podés hacer?
- 🧭 Comparar jugadores con gráficos **Radar**
- 🐝 Visualizar su posición relativa con **Beeswarm plots**
- 📈 Analizar relaciones técnicas entre métricas con **Scatter plots**

Seleccioná una opción desde el menú lateral izquierdo para comenzar.
""")
# Footer
from utils.footer import mostrar_footer

mostrar_footer()