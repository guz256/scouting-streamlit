from mplsoccer import Radar
import pandas as pd

def crear_radar(params):
    """
    Crea una instancia de Radar con parámetros comunes.
    """
    return Radar(
        params=params,
        min_range=[0] * len(params),
        max_range=[100] * len(params),
        round_int=[False] * len(params),
        num_rings=4,
        ring_width=1,
        center_circle_radius=1
    )

def extraer_valores(df: pd.DataFrame, jugador: str, columnas: list) -> list:
    """
    Extrae los valores normalizados (percentiles) para un jugador dado.
    """
    fila = df[df['Jugador'] == jugador]
    if fila.empty:
        return [0] * len(columnas)
    return fila[columnas].astype(float).values.flatten().tolist()

def aplicar_estilo_radar(ax, jugador1, jugador2):
    """
    Aplica estilo y etiquetas comunes al radar comparativo.
    """
    ax.text(0.2, 1.1, jugador1, fontsize=12, ha='center', va='center',
            transform=ax.transAxes, fontfamily='monospace', color='#0059b3')
    ax.text(0.8, 1.1, jugador2, fontsize=12, ha='center', va='center',
            transform=ax.transAxes, fontfamily='monospace', color='#cc3333')

    ax.text(0, -0.1, 'Percentiles calculados por posición y torneo', fontsize=10,
            ha='left', va='center', transform=ax.transAxes,
            fontfamily='monospace', color='#6C969D')
    return ax
