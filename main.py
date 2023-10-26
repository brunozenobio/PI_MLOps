#from funciones import *
from fastapi import FastAPI

app = FastAPI()

@app.get('/home')
def saludar():
    return "Hola funciono"

'''
@app.get('/developer')
def developer(desarrollador:str):
    try:
        return developer_func(desarrollador)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/user')
def userdata(desarrollador:str):
    try:
        return userdata_func(desarrollador)
    except Exception as e:
        return {"Error":str(e)}
    
@app.get('/genero')
def UserForGenre(desarrollador:str):
    try:
        return UserForGenre_func(desarrollador)
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
'''