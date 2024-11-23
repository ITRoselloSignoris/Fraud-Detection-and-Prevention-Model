# Proyecto final - Detección y Prevención de Fraude
## Descripción del Proyecto
### <u>Objetivo </u>
En este proyecto, voy a realizar un modelo de clasificación con Random Forest para detectar y prevenir fraudes a partir de los clientes ficticios de una empresa de comercio electrónico.  
_<u>Los datos de entrada que se le van a pasar al modelo para hacer la predicción son:</u>_
- `orderAmount`: Float
- `orderState`: String
- `paymentMethodRegistrationFailure`: String
- `paymentMethodType`: String
- `paymentMethodProvider`: String
- `paymentMethodIssuer`: String
- `transactionAmount`: Integer
- `transactionFailed`: Bool
- `emailDomain`: String
- `emailProvider`: String
- `customerIPAddressSimplified`: String
- `sameCity`: String  

_<u>Y le vamos a devolver una de las siguientes predicciones:</u>_
- __No__
- __Sí__
- __Warning__
### <u>Proceso</u>
Vamos a recibir un dataset en formato JSON, el cual lo tenemos que __transformar__ a un formato CSV.  
Luego de realizar esta transformación, podemos observar columnas que deberíamos eliminarlas o manipularlas. Por ejemplo, los identificadores deberíamos eliminarlos, y en la columna `CustomerEmail` nos tenemos que quedar con los valores más importantes/comunes y luego clasificar los valores raros con un valor nuevo llamado _"weird"_.  

Luego de este proceso de adaptación y manipulación de datos, hacemos un __Análisis Exploratorio de Datos (EDA)__, donde hacemos análisis univariado, análisis bivariado y correlaciones, de ciertas variables que nos llamaron la atención. Habiendo realizado el EDA, resalté ciertas observaciones que pude encontrar.  

Después de haber hecho el EDA, realizamos la __preparación de datos__ donde discretizamos variables, tratamos nulos e interpretamos y modificamos ciertas variables.  

Previo al entrenamiento, seleccionamos ciertas columnas del dataset post procesado y normalizamos los valores dentro de ellas. A la hora del entrenamiento, vamos a entrenar 2 modelos de __Clustering__ con 2 algoritmos distintos: Un modelo usa el algoritmo de __K-Means__ y otro el de __HDBSCAN__. Luego de haberlos entrenado, a través de un gráfico de coordenadas plasmo las observaciones encontradas para cada modelo.  

Para finalizar con el modelado, vamos a realizar una __modelo de clasificación con Random Forest__. Una vez entrenado el modelo con ciertos parámetros, realizamos una matriz de confusión para poder observar la cantidad de predicciones correctas e incorrectas del modelo, organizadas por clase.

Pasando al __desarrollo de la API__, creamos una API que reciba ciertos datos de entrada, los transforme (discretización,one hot encoding) y devuelva la predicción del modelo en base a esos datos de entrada. Luego creamos un contenedor con Docker de la API. Finalmente, la alojamos en Microsoft Azure. 

Por último, creamos con Gradio una __interfaz gráfica interactiva__ y la alojamos en Hugging Face Space. La URL para la app interactiva es la siguiente: https://huggingface.co/spaces/Itrs/Proyecto_Final

## Métodos Usados
- Limpieza y Transformación de Datos (Data Wrangling)
- Análisis Exploratorio de los Datos (EDA)
- Visualización de Datos
- Preparación de Datos
- Entrenamiento de Modelo (Clustering y Clasificación)
- Evaluación de Modelo
- Despliegue de Modelo con una API, Docker y Microsoft Azure
- Interfaz Gráfica del Usuario con Gradio

## Tecnologías y Herramientas Utilizadas
### <ins>1. Limpieza, Transformación y Preparación de Datos </ins> 
- **Pandas**: Cargar y preparar datos, manipular conjuntos de datos eficientemente, transformación de dataset en formato JSON a formato CSV, realizar análisis descriptivo.

### <ins>2. Visualización de Datos / EDA</ins>
- **Funpymodeling**: Observar distribución de los datos, cantidad de valores únicos y la cantidad de apariciones de cada uno, desvío estándar, porcentaje de nulos, correlación entre variables, entre otra información.
- **Seaborn y Matplotlib**: Herramientas para la visualización de datos y creación de gráficos estadísticos (Correlación, gráficos de dipersión, matriz de confusion).
- **Minepy (MINE)**: Identificar relaciones no lineales y complejas entre variables en conjuntos de datos con el algoritmo MINE (Maximal Information-based Nonparametric Exploration).
- **YellowBrick (Cluster.KelbowVisualizer)**: Visualización del método del codo en algoritmos de clustering.
- **Plotly (Scatter3D)**: Visualización de gráfico interactivo 3D de dispersión para clusters.

### <ins>3. Modelado</ins>
- **Hdbscan**: Algoritmo de HDBSCAN para Modelo de Clustering.
- **Scikit-Learn**
    - **KMeans**: Algoritmo de K-Means para Modelo de Clustering.
    - **RandomForestClassifier**: Algoritmo de Random Forest para Modelo de Clasificación.
    - **ConfusionMatrixDisplay**: Visualizar Matriz de Confusión para el Modelo de Clasificación.
- **Mlflow**: Gestión y registro de experimentos de modelos, permitiendo rastrear parámetros, métricas y versiones.

### <ins>4. API</ins>
- **FastAPI**: Creación de una API para exponer el modelo entrenado.
- **Uvicorn**: Servidor ASGI ligero y rápido que permite ejecutar la API asíncronamente.
- **Requests**: Hacer solicitudes HTTP a la API.
- **Pydantic**: Validar los datos de entrada de la API.
- **Gradio**: Interfaz gráfica interactiva que permite a los usuarios probar el modelo visualmente.

### <ins>5. Deployment</ins> 
- **Docker**: Contenerizar la API y simplificar su despliegue.
- **Hugging Face Space**: Alojar y compartir el modelo de manera centralizada.
- **Microsoft Azure**: Plataforma de despliegue para alojar la API.

### <ins>Lenguaje de Programación</ins>
- **Python**: Lenguaje principal para el desarrollo del proyecto, compatible con las bibliotecas de ciencia de datos y machine learning.

## Instalación
### Docker
1. Crear imagen:  
`docker build -t proyecto_final .`

2. Crear contenedor:  
`docker run -p 7860:7860 -e ID_USER=Iñaki proyecto_final` 

## Deploy Docker Hub + Web App en Microsoft Azure 
![](imgs/DockerHub+WebApp1.png)
![/docs](imgs/DockerHub+WebApp2.png)

## A tener en cuenta
- Si queremos ejecutar `mlflow ui`, debemos estar ubicados en la carpeta __deployment/__, que es donde se encuentra la carpeta __mlruns/__ .
