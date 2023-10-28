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
    try:
        return developer_func(desarrollador)
    except Exception as e:
        return {"Error":str(e)}
  
@app.get('/user{user}')
def userdata(user:str):
    try:
        return userdata_func(user)
    except Exception as e:
        return {"Error":str(e)}
    
    


@app.get('/genero')
def UserForGenre(genero:str):
    try:
        return UserForGenre_func(genero)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/best_developer_year/{year}')   
def best_developer_year(year:int):
    try:
        return best_developer_year_func(year)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/recommend/{developer_rec}') 
def developer_rec(developer_rec:str):
    try:
        return developer_rec_func(developer_rec)
    except Exception as e:
        return {"Error":str(e)}


@app.get('/recomendacion_games/{user}') 
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
