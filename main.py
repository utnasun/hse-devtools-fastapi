from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime 
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "Hello, dog person!"

@app.post('/post', response_model=Timestamp)
def post():
    post = Timestamp(
        id = post_db[-1].id + 1,
        timestamp = int(datetime.now().timestamp())
    )
    post_db.append(post)
    return post

@app.get('/dog', response_model=List[Dog])
def get_dogs(kind: DogType):
    if kind:
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    return list(dogs_db.values())


@app.post('/dog', response_model=Dog)
def create_dog(dog: Dog):
    if dog.pk in dogs_db:
        raise HTTPException(status_code=409, detail="The specified PK already exists.")
    dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{pk}', response_model=Dog)
def get_dog_by_pk(pk: int):
    if pk in dogs_db:
        return dogs_db[pk]
    else:
        raise HTTPException(status_code=404, detail={"msg": f'There is no dog with specified PK {pk}'})

@app.patch('/dog/{pk}', response_model=Dog)
def update_dog_by_pk(pk: int, dog: Dog):
    for key, value in dogs_db.items():
        if value.pk == pk and dog.pk == pk:
            dogs_db[key] = dog 
            return dog 
    raise HTTPException(status_code=404, detail={"msg": f'Dog with specified PK {pk} not found'})



