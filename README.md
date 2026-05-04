# Descripción del propósito del dataset
El presente análisis se fundamenta en el dataset BoT-IoT, un repositorio especializado en tráfico de red generado en entornos de Internet de las Cosas (IoT). El archivo fuente, denominado DDoSdata.csv, tiene un peso aproximado de 588 MB, lo que permite un estudio volumétrico real de incidentes de ciberseguridad a gran escala.

1.1. Estructura y Composición
El conjunto de datos integra un total de 47 variables que documentan el comportamiento del tráfico de red. Estas se dividen en tres categorías principales:

Datos de Identificación: Registran los puntos de origen y destino mediante direcciones IP (saddr, daddr) y puertos de comunicación (sport, dport).

Métricas de Rendimiento: Documentan el volumen de la transmisión, incluyendo el conteo de paquetes (pkts), el tamaño de la carga útil en bytes (bytes) y la duración temporal de cada flujo (dur).

Etiquetado Forense: El dataset incluye etiquetas de clasificación (attack, category, subcategory) que permiten diferenciar de manera inequívoca el tráfico legítimo de las actividades maliciosas.

1.2. Escenario del Incidente
Los registros analizados capturan un ataque de Denegación de Servicio Distribuido (DDoS). El tráfico malicioso está orientado principalmente a saturar servicios web (Puerto 80) utilizando vectores de ataque basados en protocolos TCP y UDP. La muestra es representativa de un entorno de infraestructura crítica donde múltiples dispositivos zombis (botnets) coordinan ráfagas de datos para comprometer la disponibilidad de un nodo central.

1.3. Propósito del Análisis
El objetivo de procesar este dataset es caracterizar los patrones matemáticos del ataque para facilitar el diseño de sistemas de detección de intrusiones (IDS). Dada la alta densidad de registros, el archivo permite evaluar la eficiencia de procesamiento de datos y la capacidad de respuesta de modelos predictivos ante inundaciones de tráfico anómalo.

## DESCRIPCION DEL PROYECTO
Este proyecto tiene como objetivo realizar un análisis exploratorio de datos (EDA) y la visualización de información relevante a partir de un dataset, aplicando técnicas de tratamiento de datos con Python.
## Resumen de las anomalías encontradas
Resumen de anomalías detectadas
Se identificaron 38,338 conexiones anómalas (~2% del total) mediante Isolation Forest, caracterizadas por patrones repetitivos y alta frecuencia.
Se observó una concentración extrema de tráfico hacia la IP 192.168.100.3, lo que indica un posible objetivo de ataque.
Las IPs de origen más activas fueron:
192.168.100.147
192.168.100.148
192.168.100.149
192.168.100.150
Estas generaron cientos de miles de conexiones, comportamiento no típico de tráfico normal.
El tráfico se concentró principalmente en el puerto 80 (HTTP), indicando un posible ataque tipo HTTP Flood (DDoS).
Mediante clustering (K-Means y DBSCAN), se identificaron IPs con comportamiento anómalo, compatibles con actividad de botnet, debido a:
alto número de conexiones
alto volumen de paquetes
baja diversidad de destinos

## GRAFICO DE DISTRIBUCION 

<img width="576" height="455" alt="output" src="https://github.com/user-attachments/assets/ee362b0d-dc02-4a9d-957e-8adcc4ada95b" />

El gráfico evidencia un desbalance extremo en el dataset, reflejando el comportamiento real de un ataque DDoS. La clase 1 (Ataques) domina casi por completo con cerca de 2 millones de paquetes, volviendo visualmente imperceptible al tráfico legítimo (clase 0). Básicamente, estamos viendo cómo la botnet inunda la red con datos basura para saturar el ancho de banda y los puertos de los equipos físicos, como los switches. A nivel de análisis, este escenario nos obliga a aplicar técnicas de balanceo antes de entrenar cualquier modelo de Machine Learning, ya que de lo contrario, el algoritmo se sesgará y simplemente predecirá todo como un ataque

## GRAFICO DE TIPOS DE ATAQUES

<img width="855" height="502" alt="tipos de ataques" src="https://github.com/user-attachments/assets/c750d226-cf79-4af7-886a-9cc4fe9924a2" />

Este gráfico por categorías confirma la naturaleza volumétrica del incidente. Al observar que la totalidad de los casi 2 millones de registros están clasificados como 'DDoS', queda en evidencia que la captura de datos refleja el punto crítico del ataque. El tráfico 'Normal' es tan mínimo 

## PROTOCOLOS DE TRAFICO

<img width="567" height="455" alt="protocolos_trafico" src="https://github.com/user-attachments/assets/db88760f-c118-4ce5-8617-6ca1b5e467e2" />

El análisis de protocolos revela que estamos ante un ataque de tipo multi-vector, dominado casi en partes iguales por TCP y UDP (rondando el millón de paquetes cada uno). La ausencia visual de otros protocolos como ARP o ICMP indica que los atacantes no están realizando simples escaneos locales o inundaciones de ping. En su lugar, la botnet está combinando dos técnicas letales de manera simultánea: ataques volumétricos brutos mediante UDP para asfixiar el ancho de banda de los enlaces, y ataques de agotamiento de estado mediante TCP para colapsar directamente los procesadores de los servidores y firewalls.


## DISTRIBUCION DE PAQUETES

<img width="576" height="455" alt="distribucion_paquetes" src="https://github.com/user-attachments/assets/3df1625c-92d9-4893-a656-d4b7d3183f0a" />

El histograma de distribución de paquetes (pkts) muestra una concentración masiva en valores extremadamente bajos, cercanos a cero. Esto confirma la eficiencia de la botnet: en lugar de enviar ráfagas de paquetes grandes que podrían ser detectadas por firewalls básicos, los atacantes optan por enviar millones de micro-paquetes de forma individual. Esta estrategia busca saturar la capacidad de procesamiento del hardware (CPU e interrupciones del sistema) en los nodos de red y dispositivos finales, confirmando que el objetivo no es solo llenar el ancho de banda, sino agotar los recursos computacionales de la infraestructura.

## CORRELACION 

<img width="1127" height="901" alt="matriz_correlacion" src="https://github.com/user-attachments/assets/881d2e43-dd62-44c7-bfe7-4fd2ab18d8db" />

La matriz identifica relaciones críticas para la detección de intrusiones. Se observa una correlación positiva perfecta entre el volumen de paquetes (pkts) y el tamaño de la carga útil (bytes), lo que confirma que el ataque satura la red mediante ráfagas constantes de datos. Asimismo, existe una vinculación directa entre las marcas de tiempo (stime, ltime) y la presencia del ataque, lo que demuestra que la actividad de la botnet fue continua y no aleatoria. Finalmente, la alta correlación entre las banderas de estado (flgs) y la variable objetivo (attack) resalta que el comportamiento anómalo de los protocolos es el mejor predictor para identificar el tráfico malicioso, permitiendo reducir las 47 variables originales a un conjunto optimizado para el modelado de Machine Learning.

## BYTES POR TIPO DE TRAFICO 

<img width="554" height="455" alt="bytes_tipo_trafico" src="https://github.com/user-attachments/assets/15c9bdd4-7d92-4f02-a800-84bcd25f4f21" />

La gráfica de cajas revela una diferencia drástica en el tamaño de los paquetes. Mientras que el tráfico normal (clase 0) presenta una alta variabilidad con múltiples valores atípicos (outliers) que alcanzan hasta los 70 millones de bytes (correspondientes a descargas o navegación legítima), el tráfico de ataque (clase 1) se mantiene comprimido cerca del cero. Esto confirma que la botnet no busca saturar la red con archivos pesados, sino con una inundación masiva de paquetes extremadamente pequeños. Esta estrategia es típica de los ataques DDoS para agotar la capacidad de procesamiento de los dispositivos de red sin necesidad de consumir grandes cantidades de ancho de banda por paquete.

# Correciones 
Pregunta para el trabajo final:

¿Qué impacto tiene la proporción de contaminación  en un modelo de Isolation Forest, y cómo influye en la detección de anomalías cuando no se conoce previamente el porcentaje real de outliers en los datos?
La proporción de contaminación en Isolation Forest define qué porcentaje de los datos el modelo va a considerar como anomalías. Esto impacta directamente en el resultado: si el valor es alto, el modelo detecta más anomalías (pero aumenta el riesgo de falsos positivos); si es bajo, detecta menos (y puede dejar pasar anomalías reales).

Cuando no se conoce el porcentaje real de outliers, este parámetro se vuelve una suposición, por lo que influye mucho en la calidad de la detección. Un valor mal elegido puede hacer que el modelo sea poco confiable, ya sea exagerando o ignorando anomalías.

Por eso, en estos casos se suele usar un valor estimado y luego ajustarlo revisando los resultados, buscando un equilibrio entre detectar correctamente las anomalías y evitar errores.




















que ni siquiera alcanza a graficarse. A nivel físico, esto demuestra que los enlaces y canales de la infraestructura estaban totalmente secuestrados por la botnet, bloqueando el paso de cualquier paquete o conexión legítima
