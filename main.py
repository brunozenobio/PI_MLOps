from funciones import *
from fastapi import FastAPI
import pandas as pd
from surprise import SVD
app = FastAPI()

@app.get('/')
def bienvenida():
    return {'API de consultas a una base de datos de Steam'}



@app.get('/developer/{desarrollador}')
def developer(desarrollador:str):
    """
    Esta funcion calcula para un desarrolador de juego devuelve la cantidad de items y el porcentaje de contenido gratis por año
    params:
    desarrollador:str Desarrolador
    """
    try:
        return developer_func(desarrollador)
    except Exception as e:
        return {"Error":str(e)}
  
@app.get('/user{user}')
def userdata(user:str):
    """
    Esta funcion devuelve para un usuario la cantida de dinero gastado la cantidad de items y el porcentaje de recomendaciones positivas del total de sus recomendaciones.
    params:
    user:str ID de un usuario
    """
    try:
        return userdata_func(user)
    except Exception as e:
        return {"Error":str(e)}
    
    


@app.get('/genero')
def UserForGenre(genero:str):
    """
    Esta funcion devuelve para un genero dado, el usuario que acumula mas horas desde el lanzamiento del juego, y la cantidad de horas totales en cada año
    params:
    genero:str Genero de un juego
    """
    try:
        return UserForGenre_func(genero)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/best_developer_year/{year}')   
def best_developer_year(year:int):
    """
    Esta funcion calcula para un año dado, el top de los  tres desarrolladores con mas juegos.
    params:
    year:int : Año
    """
    try:
        return best_developer_year_func(year)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/recommend/{developer_rec}') 
def developer_rec(developer_rec:str):
    """
    Esta funcion calcula para un desarrolador la cantidad de usuarios con reviews positivas y negativas.
    params:
    developer_rec:str : Desarrolador
    
    
    """
    try:
        return developer_rec_func(developer_rec)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/recommend_user_games/{user}') 
def ser_recommend(user:str):
    """
    Esta función recomienda los 5 mejores juegos para un usuario especificado.

    Params:
    user:str - nombre del usuario al que se le recomendarán los juegos.

    Returns:
    Diccionario con los nombres de los 5 juegos recomendados.
    """
    try:
        return user_recommend_fuc(user)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/recommend_item/{item}') 
def item_recommend(item_id:int):
    """
    Esta función recomienda 5 items  dado un item especifico.

    Params:
    item_id:int - id del item del cual se quieren recomendar

    Returns:
    Diccionario con los nombres de los 5 juegos recomendados.
    """
    try:
        return item_recommend_func(item_id)
    except Exception as e:
        return {"Error":str(e)}