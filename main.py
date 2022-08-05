from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()


# Models


class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "balck"
    blonde = "blonde"
    red = "red"


class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Cristian"
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Rojas"
    )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=28
    )
    hair_color: Optional[HairColor] = Field(default=None, example="brown")
    is_marriend: Optional[bool] = Field(default=None, example=False)


class Person(PersonBase):
    password: str = Field(
        ...,
        min_length=8,
        example="estoesunaprueba"
    )

    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Cristian",
    #             "last_name": "Rojas",
    #             "age": 27,
    #             "hair_color": "brown",
    #             "is_married": False
    #         }
    #     }


class PersonOut(PersonBase):
    pass


class Location(BaseModel):
    city: str
    state: str
    country: str


@app.get("/")
def home():
    return {"Hello": "world"}


# Request and response body

@app.post("/person/new", response_model=PersonOut)
def create_person(person: Person = Body(...)):
    return person


# Validaciones Query parameters


@app.get("/person/details")
def show_person(
        name: Optional[str] = Query(
            None,
            min_length=1,
            max_length=50,
            title="Person Name",
            description="This is the person name. It's between 1 and 50 characters",
            example="Laura"
        ),
        age: str = Query(
            ...,
            title="Person age",
            description="This is the person age. It's required",
            example="28"
        )
):

    return {name: age}


# Validaciones: Path parameters


@app.get("/person/details/{person_id}")
def show_person(
        person_id: int = Path(
            ...,
            gt=0,
            example=28
        )
):
    return {person_id: "It exist"}


# Validaciones: Reqeuest body


@app.put("/person/{person_id}")
def update_person(
        person_id: int = Path(
            ...,
            title="Person ID",
            description="This is the person ID",
            gt=0
        ),
        person: Person = Body(...),
        # location: Location = Body(...)
):
    # result = person.dict()
    # result.update(location.dict())
    return person
