import pandas as pd
from datetime import datetime
import ast
import gzip

with gzip.open('datasets/user_items_proc.csv.gz', 'rb') as f:
    users_items_proc = pd.read_csv(f, encoding='utf-8')
    
with gzip.open('datasets/users_items.csv.gz', 'rb') as f:
    users_items = pd.read_csv(f, encoding='utf-8')
    
steam_games = pd.read_csv('./datasets/steam_games.csv', parse_dates=['release_date'])
user_review = pd.read_csv('./datasets/user_reviews.csv')

def developer_func(desarrollador:str):
    if desarrollador not in steam_games['developer'].values:
        return "No se ha encontrado ese desarrollador"  # Devuelve el mensaje si no se encuentra en el DataFrame
    
    items_por_año = steam_games[steam_games['developer'].lower() == desarrollador.lower()].groupby('year')['id'].count().reset_index()
    items_por_año['Year'] = items_por_año['Year'].astype(int)
    
    # Contar juegos gratuitos (Free to Play) cuando 'price' es 0
    items_por_año_free = steam_games[(steam_games['developer'] == desarrollador) & (steam_games['price'] == '0')].groupby('Year')['id'].count().reset_index()
    items_por_año_free.rename(columns={'id': 'Free to Play'}, inplace=True)
    
    # Uno las tablas de items_por_año e items_por_año_free
    merged_data = pd.merge(items_por_año, items_por_año_free, on='Year', how='left')
    
    # Calculo el contenido gratis por año
    contenido_free = round(merged_data['Free to Play'] / merged_data['id'] * 100, 0)
    
    # Crear el DataFrame final
    resultado = {
        'Año': merged_data['year'].iloc[0],
        'Cantidad de Items': merged_data['id'].iloc[0],
        'Contenido Free': contenido_free.fillna(0).astype(str).iloc[0] + '%'  # Llenar NaN con 0 para evitar problemas
    }
    
    return resultado


def userdata_func(User_id:str):
    usuario = users_items.loc[users_items['user_id'].lower() == User_id.lower()]['items'] #---> user
    if not usuario.empty:
        usuario = usuario.iloc[0]
    else:
        return "No se ha encontrado ese Usuario"  # Devuelve el mensaje si no se encuentra en el DataFrame
    data = ast.literal_eval(usuario)
    result = pd.DataFrame(data)
    result.dropna(inplace=True)
    result['item_id'] = result['item_id'].astype(int)
    
    join = pd.merge(user_review,steam_games[['id','price']],left_on='item_id',right_on='id',how='left')
    usuario_gasto_recomendacion = join.groupby('user_id').agg({
                        'recommend':['count','sum'],
                        }).reset_index()
    usuario_gasto_recomendacion.columns = ['user_id','tot_recommend','true_recommend']
    usuario = usuario_gasto_recomendacion[usuario_gasto_recomendacion['user_id'] == User_id]
    
    join2 = pd.merge(result[['item_name']],steam_games[['app_name','price']],left_on='item_name',right_on='app_name',how='left')
    
    return {
        'Usuario X':User_id,
        'Dinero gastado':f"{join2['price'].sum()} USD",
        '% Recomendación Positiva':f"{(usuario['true_recommend'].iloc[0] / usuario['tot_recommend'].iloc[0] * 100)}%",
        'cantidad de items':join2.shape[0]
    }
    
    
def UserForGenre_func(genero:str):
    genero = genero.lower()
    steam_games_cop = steam_games
    steam_games_cop.columns = steam_games.columns.str.lower()
    generos = steam_games.drop(columns=['app_name','release_date','specs','price','id','developer','year']).columns
    if genero not in generos:
        return "No existe ese género"
    # FALTA ARREGLAR QUE EL GENERO PUEDA SER INGRESADO CON MAYUSCULAS O MINUSCULAS    
    usuarios_games = pd.merge(users_items_proc,steam_games,left_on='item_name',right_on='app_name',how='inner')
    usuarios_games = usuarios_games[usuarios_games[genero]==1]
    user_max_hor = usuarios_games.groupby(['user_id'])['playtime_forever'].sum().reset_index()
    user_max_hora = user_max_hor.loc[user_max_hor['playtime_forever'].idxmax(), 'user_id']
    usuario_hora = usuarios_games[usuarios_games['user_id'] == user_max_hora].groupby('year')['playtime_forever'].sum().reset_index()
    lista_resultados = []
    for index, row in usuario_hora.iterrows():
        if row['playtime_forever'] == 0.0:
            continue
            
        diccionario = {
            'Año':int(row['year']),
            'Horas': int(row['playtime_forever'])
        }
        lista_resultados.append(diccionario)
        
    dic = {'Usuario ':user_max_hora,'Horas Jugadas':lista_resultados}
        
    return dic