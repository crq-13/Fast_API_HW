from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Body

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

