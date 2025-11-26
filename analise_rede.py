import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

def gerar_grafico(df):
    """Retorna gráfico PNG em base64"""
    plt.figure(figsize=(15, 6))
    sns.lineplot(data=df, x='timeStamp', y='Latency')
    plt.title('Latência ao longo do tempo')
    plt.xlabel('Tempo')
    plt.ylabel('Latência (ms)')

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches='tight')
    buffer.seek(0)
    plt.close()

    return base64.b64encode(buffer.getvalue()).decode()


def analisar_csv(file_bytes):
    """Processa CSV, detecta anomalias e retorna métricas + gráfico"""

    df = pd.read_csv(BytesIO(file_bytes))

    # Converte timestamp
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='ms')

    # --- Isolation Forest ---
    X = df[['Latency', 'bytes']]
    model = IsolationForest(contamination=0.01)
    df['anomaly_if'] = model.fit_predict(X)
    anomalias_if = df[df['anomaly_if'] == -1]

    num_if = len(anomalias_if)
    percent_if = (num_if / len(df)) * 100

    # --- DBSCAN ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    dbscan = DBSCAN(eps=0.5, min_samples=10)
    df['cluster'] = dbscan.fit_predict(X_scaled)

    anomalias_db = df[df['cluster'] == -1]
    num_db = len(anomalias_db)
    percent_db = (num_db / len(df)) * 100

    # --- Gráfico ---
    grafico_base64 = gerar_grafico(df)

    # --- Retorno ---
    return {
        "total_amostras": len(df),

        "isolation_forest": {
            "anomalias": int(num_if),
            "percentual": round(percent_if, 2)
        },

        "dbscan": {
            "anomalias": int(num_db),
            "percentual": round(percent_db, 2)
        },

        "grafico_latencia_base64": grafico_base64
    }
