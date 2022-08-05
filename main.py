from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI
from fastapi import Body, Query, Path, status, Form, Header, Cookie, UploadFile, File

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


class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="crq13")
    message: str = Field(default="Succesfull")



@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"Hello": "world"}


# Request and response body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person: Person = Body(...)):
    return person


# Validaciones Query parameters


@app.get(
    path="/person/details",
    status_code=status.HTTP_200_OK
    )
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

# Forms


@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK
)
def login(username: str = Form(...), password: str = Form(...)):
    return LoginOut(username)

# Cookies and header parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK
)
def contact(
        first_name: str = Form(
            ...,
            max_length=20,
            min_length=1,
        ),
        last_name: str = Form(
            ...,
            max_length=20,
            min_length=1,
        ),
        email: EmailStr = Form(...),
        message: str = Form(
            ...,
            min_length=20
        ),
        user_agent: Optional[str] = Header(default=None),
        ads: Optional[str] = Cookie(default=None)
):
    return user_agent


@app.post(
    path="/post-image"
)
def post_image(
        image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }


