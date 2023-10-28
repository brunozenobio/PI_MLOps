import pandas as pd
import pickle
from surprise import SVD

def developer_func(desarrollador:str):
    
    
    steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
    

    steam_games.dropna(subset=['Year'],inplace=True)
    steam_games['Year'] = steam_games['Year'].astype(int)
    
    
    if desarrollador.capitalize() not in steam_games['developer'].values:
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
    

def UserForGenre_func(genero:str):
    users_gen = pd.read_csv('./datasets/max_por_gen.csv')
    if genero.lower() not in [x.lower() for x in users_gen['Género'].tolist()]:
        return "No se encontró ese genero"
    
    gen = users_gen[users_gen['Género'].str.lower() == genero.lower()]
        
    return {
        'Usuario':gen['Usuario'].tolist(),
        'Horas jugadas':gen['Año_Horas'].tolist()     
    }
    

def best_developer_year_func(year:int):
    steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    
    steam_games.dropna(inplace =True)
    steam_games['Year'] = steam_games['Year'].astype(int)
    func_4 = pd.merge(user_review,steam_games,left_on='item_id',right_on='id',how='inner')
    func_4 = func_4[func_4['Year'] ==year]
    mejores_dev = func_4.groupby('developer')['recommend'].sum().reset_index().sort_values(by='recommend',ascending=False)
    if mejores_dev.empty:
        return 'No se enocntraron reviews para items que hayan salido ese año'
    else:
        puesto1 = mejores_dev.iloc[0][0]
        puesto2 = mejores_dev.iloc[1][0]
        puesto3 = mejores_dev.iloc[2][0]
        puestos = {"Puesto 1": str(puesto1), "Puesto 2":str(puesto2), "Puesto 3": str(puesto3)}
        return puestos
    
    
def developer_rec_func(desarrolladora:str):
    steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    func_5 = pd.merge(user_review,steam_games,left_on='item_id',right_on='id',how='inner')
    func_5['developer'] = func_5['developer'].str.lower()
    
    desarrolladora = desarrolladora.lower()
    func_5 = func_5[func_5['developer'] == desarrolladora]
    if func_5.empty:
        return 'No se enocntraron reviews para items que hayan salido ese año'
    else:
        true_value = func_5[func_5['sentiment_analysis']==2]['sentiment_analysis'].count()
        false_value = func_5[func_5['sentiment_analysis']==0]['sentiment_analysis'].count()
        return {desarrolladora:[f'Negative = {int(false_value)}',f'Positive = {int(true_value)}']}
    
    
    
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
    user_reviews = pd.read_csv('./datasets/user_reviews_model.csv',usecols=['user_id','user_id_num','item_id','sentiment_analysis'])

    # Cargo la lista de juegos de steam
    df_steam = pd.read_csv('./datasets/steam_games.csv')

    user_rec = user_reviews[user_reviews['user_id'] == user]['user_id_num'].iloc[0]
    # Predecir la puntuación del usuario para cada juego
    predictions = [model.predict(user_rec, item_id) for item_id in user_reviews['item_id']]
    recommendations = sorted(predictions, key=lambda x: x.est, reverse=True) # Obtén las mejores 5 recomendaciones

    # Convertir las recomendaciones en un DataFrame de pandas
    recommendations = pd.DataFrame(recommendations)

    # Eliminar duplicados basados en el id del juego
    recommendations = recommendations.drop_duplicates(subset='iid')

    # Mergeo la lista de juegos con las recomendaciones en base al id del juego
    merge = pd.merge(df_steam[['app_name','id']],recommendations,left_on='id',right_on='iid',how='right')

    rec = merge[['app_name']].dropna()[:5].values.tolist()

    # Retornar los juegos como un diccionario
    return {
        'Recomendacion 1 ': rec[0][0],
        'Recomendacion 2 ': rec[1][0],
        'Recomendacion 3 ': rec[2][0],
        'Recomendacion 4 ': rec[3][0],
        'Recomendacion 5 ': rec[4][0]
    }
