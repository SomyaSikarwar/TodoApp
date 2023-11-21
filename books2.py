from fastapi import FastAPI, HTTPException, Form ,Header
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class book(BaseModel):
    id: UUID
    Name: str = Field(min_length=1)
    Author: str
    Description: Optional[str] = Field(min_length=1, max_length=50)  # making discription optional
    Rating: int = Field(gt=-1, lt=11)

    class Config:
        schema = {
            "example": {
                "id": "196e5fb3-a8ae-4e25-b447-d7148d160b2f",
                "Name": "Sikarwar",
                "Author": "Somya",
                "Description": "very nive book",  # making discription optional
                "Rating": 10
            }
        }


# CREATING THE RESPONSE BODY WHEN WE DO NOT NEED A PARTICULAR FIELD LIKE HERE IN CASE OF RATING(WE USE IT WHEN
# USER INPUTS ITS PASSWORD AND IN RESPONSE WE DO NOT GET THE PASSWORD )
class book_no_rating(BaseModel):
    id: UUID
    Name: str = Field(min_length=1)
    Author: str
    Description: Optional[str] = Field(min_length=1, max_length=50)  # making discription optional


app = FastAPI()

Books = []

#CREATING AN API FOR LOGIN WHICH CONTAINS USERID AND PASSWORD
@app.post("/books/login")
async def books_login(username : str = Form() , password : str = Form()):
    return {"Username" : username , "Password" : password}


@app.get("/header")
async def header(random_header : Optional[str] = Header()):
    return {"Random Header" : random_header}


@app.get("/")
async def List_books():
    if len(Books) < 1:
        dummy()
    return Books


@app.get("/book/{book_id}")
async def read_book(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x


@app.get("/Rating/{book_id}", response_model=book_no_rating)
async def read_book_no_rating(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x


# CREATING OUR OWN STATUS CODE RESPONSES USING STATUS CODE
@app.post("/", status_code=202)
async def Add_Book(Book: book):
    Books.append(Book)
    return Book


@app.put("/")
async def Update_books(book_id: UUID, Book: book):
    counter = 0
    for x in Books:
        counter += 1
        if x.id == book_id:
            Books[counter - 1] = Book
        return Books[counter - 1]
    raise caught_exception()


@app.delete("/{book_id}")
async def Delete_Book(book_id: UUID):
    count = 0
    for x in Books:
        count += 1
        if x.id == book_id:
            del Books[count - 1]
            return book_id

    raise caught_exception()


def dummy():
    book_1 = book(id="396e5fb3-a8ae-4e25-b447-d7148d160b2f",
                  Name="name_1",
                  Author="author_1",
                  Description="Description",
                  Rating=10
                  )
    book_2 = book(id="296e5fb3-a8ae-4e25-b447-d7148d160b2f",
                  Name="name_1",
                  Author="author_1",
                  Description="Description",
                  Rating=10
                  )
    book_3 = book(id="196e5fb3-a8ae-4e25-b447-d7148d160b2f",
                  Name="name_1",
                  Author="author_1",
                  Description="Description",
                  Rating=10
                  )
    Books.append(book_1)
    Books.append(book_2)
    Books.append(book_3)


# CREATING A FUNCTION FOR HANDLING EXCEPTION
def caught_exception():
    raise HTTPException(status_code='404', detail="Book Not Found!!!")
