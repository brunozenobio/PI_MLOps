from funciones import *
from fastapi import FastAPI
import pandas as pd
app = FastAPI()

@app.get('/')
def saludar():
    return "Hola funciono"


@app.get('/developer/{desarrollador}')
def developer(desarrollador:str):
    try:
        return developer_func(desarrollador)
    except Exception as e:
        return {"Error":str(e)}
  
@app.get('/user')
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
    
@app.get('/best_developer_year')   
def best_developer_year(año:str):
    try:
        return best_developer_year_func(año)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/recommend') 
def developer_rec(año:str):
    try:
        return best_developer_year_func(año)
    except Exception as e:
        return {"Error":str(e)}
