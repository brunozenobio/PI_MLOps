# PI_MLOps

<p align="center"><img src="https://user-images.githubusercontent.com/67664604/217914153-1eb00e25-ac08-4dfa-aaf8-53c09038f082.png"></p>


<h2 align="center">Proyecto Individual N°1</h2>

<h3 align="center">Machine Learning Operations (MLOps)</h3>

<h2 align="center">Bruno Zenobio, DATAFT16</h2>

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [Desarrollo](#desarrollo)
    - [ETL](#exploración-trasnformacion-y-carga-etl)
    - [EDA](#analisis-exploratorio-eda)
    - [Sistema de recomendación](#modelo-de-recomendación)
    - [Despliegue de la API](#funciones-para-la-api)

---

# Introducción
En este proyecto, llevaremos a cabo un estudio basado en Machine Learning Operations (MLOps). Este estudio se divide en tres etapas principales:

1. **Exploración y Transformación:** Se realizará un análisis exploratorio de los datos, incluyendo la exploración de distribuciones y detección de correlaciones y valores atípicos.

2. **Preparación de Datos:** Se prepararán los datos para comprender las relaciones entre las variables y construir modelos sobre ellos. También se crearán funciones para consultas a los datos, consumibles a través de una API.

3. **Modelado:** Se desarrollarán modelos de Machine Learning para entender relaciones y predecir correlaciones entre variables.

Los datos utilizados incluyen información sobre juegos en la plataforma Steam y la interacción de los usuarios con estos juegos.

<h2 align="center">Diccionario de los Datos</h2>

<p align="center"><img src="./images/Diccionario.jpg"></p>

---

# Desarrollo

### Exploración Trasnformacion Y Carga (ETL)

A partir de los 3 dataset proporcionados, staem_games,user_reviews y user_items, referentes a la plataforma de Steam, en primara instancia se realizo el proceso de limpieza de los datos.

#### `steam_games`

- Se eliminaron filas completamente nulas y se corrigieron duplicados en el ID.
- Se completaron nulos en los generos a partir de los datos de tags.
- Se completaron los valores precio cuanto este tenia un formato erroneo y era Free To Play, ademas se normalizo la columna a valores reales.
- Las variables nulas en precio (menos del 4%) se eliminaron; otras filas con valores nulos se eliminaron también, al no poder hacer un tratado mas profundo y ser una pequeña parte del dataset.
- Se crearon variables ficticias (dummies) en la columna genero para el análisis
- Se extrajo años de la columna release_date, teniendo en cuenta los distintos formatos, y las filas donde  no podia extraerse año se eliminaron
- Se eliminaron columnas no utilizadas.
- Se exporto para tener el dataset limpio

#### `user_reviews`

- Se realizo un explode ya que la columna de review era una lista de diccionarios.
- Se eliminaron filas con valores nulos en la columna de "reviews".
- Se creó una nueva columna llamada 'sentiment_analysis' usando análisis de sentimiento y se eliminó la columna de review.
- Se exporto para tener el dataset limpio


#### `user_items`
- Se realizo un explode ya que la columna de items era una lista de diccionarios.
- Se eliminaron filas con valores nulos en la columna de "items".
- Se exporto para tener el dataset limpio.

### Analisis Exploratorio (EDA)

Teniendo los 3 dataset limpios, se realizo un proceso de EDA para realizar graficos, y asi entender las estadisticas encontrar valores atipicos, y asi poder orientar un futuro analisis.

#### `steam_games`
- Primero se encontro la distribucion de los precios a partir de un grafico de cajas y bigotes, encontrados muchos valores atipicos, sin embargo considereando el contexto, no son valores necesariamente erroneos, y que se pueden encontrar juegos de centavos de dolar y juegos de miles de dolares, considerando a estos ultimos como los menos usuales.
- Se hiso un grafico de barras con los la distribucion de juegos por año añadiendo los contenidos Free, econtrando al año 2015 con la mayor cantidad de juegos y la mayor cantidad de Free.
#### `user_reviews`
- Se ralizo un grafico de barras con la cantidad de sentimientos positivos y de estos el recommend, el resultado fue que hubo muchos positivos en sentimiento seguido de los neutrales, ademas un resultado interesante es que de los positivos hay un porcentaje que no recomiendan y en los negativos un porcentaje que si, esto podria deberse a alguna falla en el analisis de sentimiento, aun asi es un porcentaje bajo.

#### `user_items`

- Para la columna playtime_forever con un diagrama de cajas y bigotes se vio la distribucio, y dio muchos atipicos, pero otro vez a falta de un mejor analisis no se hara un tratado ya que no necesariamente son erroreos, aunque si hay que verificar si hay algun valor de playtime_forever que para el item dado tiene mas horas que el año de lanzamiento del item.
- En la verificacion se encontro que no hay ningun valor que cumpla esas condiciones por esto no se modificaran estos valores.
- Tambien se calculo la dispersion entre playtime_forever y la cantidad de items.

- A partir de varias tablas, se graficaron el top de los 15 juegos con mas horas, y los 15 desarrolladores con mas horas en sus juegos.
- Tambien se graficaron los desarroladores con mas recomendaciones positivas.




### Modelo de recomendación

#### `Filtro Colaborativo`

- A partir de la tabla de user_reviews, se usaran las columnas user_id, item_id,recommend y sentiment_analysis, a partir de estas dos ultimas, se generara una nueva columna llamada rating, la cual tiene una escala entre 0 y 5.<br><br>
Se utilizo la tecnica de Desconposicion de Valor Singular(SVD) para realizar un filtro colaborativo en funcion de estas 3 columnas, se utilizo GridSearch para elegir hiperparametros optimo, el modelo final obtuvo un rmse de 0.85. En el ranking de 0 a 5 una desviacion de 0.85, si bien no es lo mas optimo es un resultado aceptable teniendo en cuenta que el ranking podria haberse elegio mas optimo. <br><br>
Puntos a mejorar para este filtro, es el hecho de haber usado otras columnas para mejorar el ranking o probar otras tecnicas como KNNBasic, ademas un filtro colaborativo teniendo en cuenta calificaciones de usuarios, podria estar sesgado a que los usuarios se inclinen mas por dar opiniones cuando estas son negativas, por esto habria que hacerse un perfil de usuari y encontrar similitudes.

#### `Filtro basado en contenido`

- Usando la tabla de steam_games, y tomando las columnas de generos como dummies, se uso la similitud coseno para calcular las similitudes entro los items, para luego a partir de uno encontrar los que tienen mas similitudes y asi poder generar las recomendaciones.<br>
Puntos a mejorar para este filtro: Usar otras columnas como desarrolador o Specs del juego, ademas no pudeo verificarse bien la performance del modelo.<br>

En generar se obtuvieron modelos aceptables, sin embargo con un analisis mas profundo se podrian haber obtenido mejores resultados.
- Algunos de estos son: Alteracion ponderada, fusion de resultados, o incluso un <b>modelo hibrido complejo</b>

### Despliegue para la API

Se desarrolaron las siguientes funciones, a las cuales se podra acceder desde la API en render.

- **`developer(desarrollador: str)`**: Retorna la cantidad de ítems y el porcentaje de contenido gratis por año para un desarrollador dado.<br>
- **`userdata(User_id: str)`**: Retorna el dinero gastado, cantidad de ítems y el porcentaje de comentarios positivos en la revisión para un usuario dado.<br>
- **`UserForGenre(género: str)`**: Retorna al usuario que acumula más horas para un género dado y la cantidad de horas por año.<br>
- **`best_developer_year(año: int)`**: Retorna los tres desarrolladores con más juegos recomendados por usuarios para un año dado.<br>
- **`developer_rec(desarrolladora: str)`**: Retorna una lista con la cantidad de usuarios con análisis de sentimiento positivo y negativo para un desarrollador dado.<br>
- **`ser_recommend(user:str)`** : Esta función recomienda  5  juegos para un usuario especificado usando un filtro colaborativo.<br>
- **`item_recommend(item:int)`** :Esta función recomienda 5 items  dado un item especifico usando un filtro basado en contenido.


