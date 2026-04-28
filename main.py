import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest

# =========================
# 1. CARGA DE DATOS
# =========================
df = pd.read_csv("DDoSdata.csv")

print("Shape inicial:", df.shape)
print(df.head())

# =========================
# 2. LIMPIEZA DE DATOS
# =========================

# Eliminar duplicados
df = df.drop_duplicates()

# Eliminar columnas irrelevantes (IDs repetidos)
df = df.drop(columns=["pkSeqID"], errors="ignore")

# Convertir timestamps
df['stime'] = pd.to_datetime(df['stime'], unit='s', errors='coerce')
df['ltime'] = pd.to_datetime(df['ltime'], unit='s', errors='coerce')

# Manejo de nulos
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna()

print("Shape después de limpieza:", df.shape)

# =========================
# 3. FEATURE ENGINEERING
# =========================

# Duración en segundos (validación)
df['duration_calc'] = (df['ltime'] - df['stime']).dt.total_seconds()

# Ratio paquetes por segundo
df['pkts_rate'] = df['pkts'] / (df['duration_calc'] + 1e-5)

# Ratio bytes por paquete
df['bytes_per_pkt'] = df['bytes'] / (df['pkts'] + 1e-5)

# =========================
# 4. EDA (ANÁLISIS EXPLORATORIO)
# =========================

print("\n=== Estadísticas ===")
print(df.describe())

# Distribución de variables clave
features = ['pkts', 'bytes', 'rate', 'dur', 'pkts_rate']

for col in features:
    plt.figure()
    sns.histplot(df[col], bins=50, kde=True)
    plt.title(f"Distribución de {col}")
    plt.show()

# Correlación
plt.figure(figsize=(10,8))
sns.heatmap(df[features].corr(), annot=True, cmap='coolwarm')
plt.title("Correlación entre variables")
plt.show()

# =========================
# 5. ANÁLISIS ESPECÍFICO DDoS
# =========================

print("\n=== Análisis DDoS ===")

# Top IPs origen (posibles atacantes)
top_src = df['saddr'].value_counts().head(10)
print("\nTop Source IPs:\n", top_src)

# Top IPs destino (posibles víctimas)
top_dst = df['daddr'].value_counts().head(10)
print("\nTop Destination IPs:\n", top_dst)

# Tráfico por puerto destino
top_ports = df['dport'].value_counts().head(10)
print("\nTop Destination Ports:\n", top_ports)

# =========================
# 6. DETECCIÓN DE ANOMALÍAS
# =========================

# Selección de features relevantes
anomaly_features = [
    'pkts', 'bytes', 'dur', 'rate',
    'srate', 'drate', 'pkts_rate', 'bytes_per_pkt'
]

X = df[anomaly_features]

# Normalización
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Modelo Isolation Forest
model = IsolationForest(contamination=0.02, random_state=42)
df['anomaly'] = model.fit_predict(X_scaled)

# -1 = anomalía, 1 = normal
df['anomaly_label'] = df['anomaly'].apply(lambda x: "Anomaly" if x == -1 else "Normal")

print("\nConteo de anomalías:")
print(df['anomaly_label'].value_counts())

# =========================
# 7. VISUALIZACIÓN DE ANOMALÍAS
# =========================

plt.figure()
sns.scatterplot(
    x=df['pkts'],
    y=df['rate'],
    hue=df['anomaly_label']
)
plt.title("Anomalías en tráfico de red")
plt.show()

# =========================
# 8. INSIGHT CLAVE
# =========================

anomalies = df[df['anomaly_label'] == "Anomaly"]

print("\n=== Posibles ataques DDoS detectados ===")
print(anomalies[['saddr', 'daddr', 'pkts', 'rate', 'dur']].head())

# Guardar resultados
df.to_csv("resultado_analisis_ddos.csv", index=False)