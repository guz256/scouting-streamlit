import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    df = pd.read_csv("data/primera_segunda_percentiles.csv")
    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().astype(str).str.replace(",", ".")
        if sample.str.match(r"^\d+(\.\d+)?$").all():
            df[col] = pd.to_numeric(sample, errors="coerce")
    return df

def filtros_sidebar(df):
    st.sidebar.header("🎯 Filtros generales")

    posiciones = sorted(df["Posición"].dropna().unique())
    pos_sel = st.sidebar.selectbox("Posición", posiciones)

    torneos = sorted(df["Torneo"].dropna().unique())
    torneos_sel = st.sidebar.multiselect("Torneo", torneos, default=torneos)

    edad_min, edad_max = int(df["Edad"].min()), int(df["Edad"].max())
    edad_sel = st.sidebar.slider("Edad", min_value=edad_min, max_value=edad_max, value=(edad_min, edad_max))

    min_min, min_max = int(df["Minutos jugados"].min()), int(df["Minutos jugados"].max())
    min_sel = st.sidebar.slider("Minutos Jugados", min_value=min_min, max_value=min_max, value=(min_min, min_max))

    df_filtrado = df[
        (df["Posición"] == pos_sel) &
        (df["Torneo"].isin(torneos_sel)) &
        (df["Edad"].between(*edad_sel)) &
        (df["Minutos jugados"].between(*min_sel))
    ]
    return df_filtrado