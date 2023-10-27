import pandas as pd




def developer_func(desarrollador:str):
    
    
    steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
    

    steam_games.dropna(subset=['Year'],inplace=True)
    steam_games['Year'] = steam_games['Year'].astype(int)
    
    
    if desarrollador not in steam_games['developer'].values:
        return "No se ha encontrado ese desarrollador"  # Devuelve el mensaje si no se encuentra en el DataFrame
    
    items_por_año = steam_games[steam_games['developer'].str.lower() == desarrollador.lower()].groupby('Year')['id'].count().reset_index()
    #items_por_año['Year'] = items_por_año['Year'].astype(int)
    
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
        ' de recomendación': str(porcentaje_recomendaciones_numerico.iloc[0]),
        'Cantidad de items': str(user['items_count'].iloc[0])
    }
    return resultado
    

def UserForGenre_func(genero:str):
    users_gen = pd.read_csv('./datasets/max_por_gen.csv')
    if genero.lower() in [x.lower() for x in df_resultados['Género'].tolist()]:
        return "No se encontró ese genero"
    
    gen = users_gen[users_gen['Género'].str.lower() == genero]
        
    return {
        'Usuario':gen['Usuario'].tolist(),
        'Horas jugadas':gen['Año_Horas'].tolist()     
    }
    
    
    

def best_developer_year_func(año:int):
    steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
    user_review = pd.read_csv('./datasets/user_reviews.csv')
    
    func_4 = pd.merge(user_review,steam_games,left_on='item_id',right_on='id',how='inner')
    func_4 = func_4[func_4['Year'] ==float(año)]
    mejores_dev = func_4.groupby('developer')['recommend'].sum().reset_index().sort_values(by='recommend',ascending=False)
    if mejores_dev.empty:
        return 'No se enocntraron reviews para items que hayan salido ese año'
    else:
        puesto1 = mejores_dev.iloc[0][0]
        puesto2 = mejores_dev.iloc[1][0]
        puesto3 = mejores_dev.iloc[2][0]
        puestos = {"Puesto 1": puesto1, "Puesto 2": puesto2, "Puesto 3": puesto3}
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
    
    
        
