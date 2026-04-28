# tratamientodatosdataset

## Descripción del trabajo 

Este proyecto tiene como objetivo realizar un análisis exploratorio de datos (EDA) y la visualización de información relevante a partir de un dataset, aplicando técnicas de tratamiento de datos con Python.

##GRAFICOS DE DISTRIBUCION 

<img width="576" height="455" alt="output" src="https://github.com/user-attachments/assets/ee362b0d-dc02-4a9d-957e-8adcc4ada95b" />

El gráfico evidencia un desbalance extremo en el dataset, reflejando el comportamiento real de un ataque DDoS. La clase 1 (Ataques) domina casi por completo con cerca de 2 millones de paquetes, volviendo visualmente imperceptible al tráfico legítimo (clase 0). Básicamente, estamos viendo cómo la botnet inunda la red con datos basura para saturar el ancho de banda y los puertos de los equipos físicos, como los switches. A nivel de análisis, este escenario nos obliga a aplicar técnicas de balanceo antes de entrenar cualquier modelo de Machine Learning, ya que de lo contrario, el algoritmo se sesgará y simplemente predecirá todo como un ataque

## GRAFICO DE TIPOS DE ATAQUES

<img width="855" height="502" alt="tipos de ataques" src="https://github.com/user-attachments/assets/c750d226-cf79-4af7-886a-9cc4fe9924a2" />

Este gráfico por categorías confirma la naturaleza volumétrica del incidente. Al observar que la totalidad de los casi 2 millones de registros están clasificados como 'DDoS', queda en evidencia que la captura de datos refleja el punto crítico del ataque. El tráfico 'Normal' es tan mínimo que ni siquiera alcanza a graficarse. A nivel físico, esto demuestra que los enlaces y canales de la infraestructura estaban totalmente secuestrados por la botnet, bloqueando el paso de cualquier paquete o conexión legítima
