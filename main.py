from funciones import *
from fastapi import FastAPI

app = FastAPI()

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