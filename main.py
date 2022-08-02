from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body, Query

app = FastAPI()

#Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_marriend: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "world"}

# Request and response body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones Query parameters

@app.get("/person/details")
def sow_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
                ):
    return {name: age}

