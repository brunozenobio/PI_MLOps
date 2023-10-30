import pandas as pd
import pickle
from surprise import SVD
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np

####### FUNCION 1 ########
def developer_func(desarrollador:str):
    """
    Esta funcion calcula para un desarrolador de juego devuelve la cantidad de items y el porcentaje de contenido gratis por año
    params:
    desarrollador:str
    """
    
    
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    

    steam_games.dropna(subset=['Year'],inplace=True)
    steam_games['Year'] = steam_games['Year'].astype(int)
    
    
    if desarrollador.strip().lower() not in list(steam_games['developer'].str.strip().str.lower()):
        return "No se ha encontrado ese desarrollador"  # Devuelve el mensaje si no se encuentra en el DataFrame
    
    items_por_año = steam_games[steam_games['developer'].str.lower() == desarrollador.lower()].groupby('Year')['id'].count().reset_index()
    
    
    # Cuento juegos gratuitos (Free to Play) cuando 'price' es 0
    items_por_año_free = steam_games[(steam_games['developer'] == desarrollador) & (steam_games['price'] == 0.0)].groupby('Year')['id'].count().reset_index()
    items_por_año_free.rename(columns={'id': 'Free to Play'}, inplace=True)
    
    # Uno las tablas de items_por_año e items_por_año_free
    merged_data = pd.merge(items_por_año, items_por_año_free, on='Year', how='left')
    
    # Calculo el contenido gratis por año
    contenido_free = round(merged_data['Free to Play'] / merged_data['id'] * 100, 2)
    
    # Creo el DataFrame final
    resultado = {
        'Año': merged_data['Year'].tolist(),
        'Cantidad de Items': merged_data['id'].tolist(),
        'Contenido Free': f'{contenido_free.fillna(0).tolist()} %'  # Llenar NaN con 0 para evitar problemas
    }
    
    return resultado

####### FUNCION 2 ########
def userdata_func(User_id:str):
    items_reviews_users = pd.read_csv('datasets/items_reviews_users.csv')
    user = items_reviews_users[items_reviews_users['user_id'].str.lower() == User_id.lower()]
    if user.empty:
        return "Usuario no encontrado"
    
    porcentaje_recomendaciones_numerico = user["porcentaje_recomendaciones_true"]
    
    resultado =  {
        'Usuario X': str(user['user_id'].iloc[0]),
        'Dinero gastado': f'{str(user["price"].iloc[0])} USD',
        'Porcentaje de recomendación': str(porcentaje_recomendaciones_numerico.iloc[0]),
        'Cantidad de items': str(user['items_count'].iloc[0])
    }
    return resultado

    
####### FUNCION 3 ########

def UserForGenre_func(genero:str):
    users_gen = pd.read_csv('./datasets/max_por_gen.csv')
    if genero.lower() not in [x.lower() for x in users_gen['Género'].tolist()]:
        return "No se encontró ese genero"
    
    gen = users_gen[users_gen['Género'].str.lower() == genero.lower()]
        
    return {
        'Usuario':gen['Usuario'].tolist(),
        'Horas jugadas':gen['Año_Horas'].tolist()     
    }
    
    
####### FUNCION 4 ########
"""
Esta función toma un año como entrada y devuelve los desarrolladores con la mayor cantidad de recomendaciones en ese año. 
Para esto, utiliza dos conjuntos de datos: 'steam_games.csv' (contiene información sobre los juegos) y 'user_reviews.csv' 
(contiene las reseñas de los usuarios para los juegos). Primero, los juegos con valores faltantes se eliminan, luego, el año 
de lanzamiento de los juegos se convierte en un entero. Los dos conjuntos de datos se unen en 'id' y se filtran para obtener 
solo los juegos lanzados en el año dado. A continuación, se agrupan los datos por desarrollador y se cuentan las recomendaciones 
para cada desarrollador. Si ningún desarrollador tiene revisiones en ese año, devuelve un mensaje indicando que no se encontraron 
revisiones para los juegos lanzados en ese año. En caso contrario, devuelve los tres primeros desarrolladores con más recomendaciones.
"""
def best_developer_year_func(year:int):
    # Carga los datos de los juegos de steam
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    # Carga las revisiones de los usuarios
    user_review = pd.read_csv('./datasets/user_reviews.csv')

    # Elimina las filas con valores faltantes en los datos de los juegos
    steam_games.dropna(inplace =True)
    # Convierte el año de lanzamiento a int
    steam_games['Year'] = steam_games['Year'].astype(int)
    # Une los datos de los juegos y las revisiones en 'id'
    func_4 = pd.merge(user_review,steam_games,left_on='item_id',right_on='id',how='inner')
    # Filtra los datos para obtener solo los juegos lanzados en el año dado
    func_4 = func_4[func_4['Year'] ==year]
    # Agrupa los datos por desarrollador 
    mejores_dev = func_4.groupby('developer')['recommend'].sum().reset_index().sort_values(by='recommend',ascending=False)
    # Verifica si no se encontraron desarrolladores con revisiones en ese año.
    if mejores_dev.empty:
        return 'No se encontraron reviews para items que hayan salido ese año'
    else:
        # Obtiene los tres primeros desarrolladores con más recomendaciones
        puesto1 = mejores_dev.iloc[0][0]
        puesto2 = mejores_dev.iloc[1][0]
        puesto3 = mejores_dev.iloc[2][0]
        puestos = {"Puesto 1": str(puesto1), "Puesto 2":str(puesto2), "Puesto 3": str(puesto3)}
        # Devuelve los tres primeros desarrolladores con más recomendaciones
        return puestos
    
    
####### FUNCION 5 ########
def developer_rec_func(desarrolladora:str):
    """
    Esta función devuelve el conteo de análisis de sentimientos para los juegos de un desarrollador específico.
    Los "sentimientos" que cuenta son análisis de sentimiento positivo y el análisis de sentimiento negativo.

    Argumentos:
    desarrolladora: str - El nombre del desarrollador del que se van a contar los análisis de sentimientos.
    """
    # Leer el archivo csv y guardar datos en steam_games
    steam_games = pd.read_csv('./datasets/steam_games.csv')
    # Leer el archivo csv y guardar datos en user_review
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    # Merging los dos datasets, con una combinación interna en sus respectivos 'id'
    func_5 = pd.merge(user_review,steam_games,left_on='item_id',right_on='id',how='inner')
    # Convertir todos los nombres de los desarrolladores en letras minúsculas para evitar la duplicación de datos debido a las diferencias de mayúsculas y minúsculas
    func_5['developer'] = func_5['developer'].str.lower()

    # Convertir el nombre del desarrollador proporcionado en letras minúsculas
    desarrolladora = desarrolladora.lower()
    # Filtrar por desarrollador
    func_5 = func_5[func_5['developer'] == desarrolladora]
    # Verificar si se encuentra los juegos del desarrollador en el dataset
    if func_5.empty:
        # En caso de que no se encuentre, se muestra mensaje indicando que no hay comentarios para este desarrollador
        return 'No se enocntraron reviews para ese desarrollador'
    # En caso contrario, contar los sentimientos de análisis de comentarios
    # Cuenta los comentarios positivos
    true_value = func_5[func_5['sentiment_analysis']==2]['sentiment_analysis'].count()
    # Cuenta los comentarios negativos
    false_value = func_5[func_5['sentiment_analysis']==0]['sentiment_analysis'].count()
    # Devolver conteos en un diccionario
    return {desarrolladora:[f'Negative = {int(false_value)}',f'Positive = {int(true_value)}']}
    
    

####### FUNCION 6 ########
    
def user_recommend_fuc(user:str):
    """
    Esta función recomienda los 5 mejores juegos para un usuario especificado.

    Params:
    user:str - nombre del usuario al que se le recomendarán los juegos.

    Returns:
    Diccionario con los nombres de los 5 juegos recomendados.
    """

    # Abrir y cargar el modelo SVD de archivos
    with open('./model/SVD_model.pkl', 'rb') as archivo:
        model = pickle.load(archivo)

    # Cargo las reseñas de usuarios 
    user_reviews = pd.read_csv('./datasets/user_reviews_model.csv',usecols=['user_id','user_id_num','item_id'])
    # Si no encuentra al usuario lo busca en items al usuario con mas horas y recomienda en base a la funcion de recomendacion por items.
    if  not user_reviews['user_id'].eq(user).any():
        user_item_max_horas = pd.read_csv('./datasets/user_item_max_horas.csv')
        if  not user_item_max_horas['user_id'].eq(user).any():
            return 'Ese usuario no existe en la base de datos.'
        else:
            item = user_item_max_horas.loc[user_item_max_horas['user_id'] == user,'item_id']
            item_recommend_func(item)
    # Cargo la lista de juegos de steam
    df_steam = pd.read_csv('./datasets/steam_games.csv')
    user_reviews_id = user_reviews[user_reviews['user_id'] != user]
    user_game = pd.merge(df_steam[['id','app_name']],user_reviews_id,left_on='id',right_on='item_id',how='inner')
    user_rec = user_reviews[user_reviews['user_id'] == user]['user_id_num'].iloc[0]
    # Predecir la puntuación del usuario para cada juego
    predicciones = pd.DataFrame()
    predicciones['app_name'] = user_game['app_name']
    predicciones['score'] = user_game['id'].apply(lambda x:model.predict(user_rec,x).est)
    predicciones.sort_values(by='score',ascending=False,inplace=True)
    # recommendations = sorted(predictions, key=lambda x: x.est, reverse=True) 

    # Convertir las recomendaciones en un DataFrame de pandas

    # Eliminar duplicados basados en el id del juego

    # Mergeo la lista de juegos con las recomendaciones en base al id del juego

    #rec = merge[['app_name']].dropna()[:5].values.tolist()
    predicciones.dropna(inplace=True)
    predicciones.drop_duplicates(subset='app_name',inplace=True)
    top_5 = predicciones.head(5)
    # Retornar los juegos como un diccionario
    return {
        'Recomendacion 1 ': top_5['app_name'].iloc[0],
        'Recomendacion 2 ': top_5['app_name'].iloc[1],
        'Recomendacion 3 ': top_5['app_name'].iloc[2],
        'Recomendacion 4 ': top_5['app_name'].iloc[3],
        'Recomendacion 5 ': top_5['app_name'].iloc[4]
    }
    
    
    
####### FUNCION 7 ########

def item_recommend_func(item_id):
    # Cargar datos relevantes desde un archivo CSV.
    perfiles_items_df = pd.read_csv('./datasets/data_standar_nearest_model.csv')
    
    if not perfiles_items_df['id'].eq(item_id).any():
        return 'Ese id no pertenece a un item registrado'
    else:
        item_name = perfiles_items_df.loc[perfiles_items_df['id'] == item_id, 'app_name'].iloc[0]

    # Eliminar la columna 'app_name' de los datos.
    data_model = perfiles_items_df.drop(['app_name'], axis=1)

    # Inicializar y ajustar el escalador de características.
    scaler = StandardScaler()
    data_standar = scaler.fit_transform(data_model)

    # Importamos modelo preentrenado de KNN
    with open('./model/NearestNeighnors.pkl', 'rb') as file:  
        knn_model = pickle.load(file)

    # Obtener el índice del artículo basado en su nombre.
    
    item_index = perfiles_items_df[perfiles_items_df['app_name'] == item_name].index[0]

    # Recuperar los vecinos más cercanos al artículo especificado.
    distances, indices = knn_model.kneighbors([data_standar[item_index]])

    # Crear un diccionario para almacenar las recomendaciones.
    recomendaciones = {}
    for i in range(1, len(indices[0])):  # Ignorar el primer vecino (ya que es el artículo mismo).
        # Identificar el índice y el nombre del artículo recomendado.
        recommended_item_index = indices[0][i]
        recommended_item_name = perfiles_items_df.loc[recommended_item_index, 'app_name']
        # Agregar recomendación al diccionario.
        recomendaciones[f"Recomendacion {i}"] = recommended_item_name

    # Devolver las recomendaciones como resultado.
    return recomendaciones