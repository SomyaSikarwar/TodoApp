from fastapi import FastAPI
from enum import Enum

app = FastAPI()


books = {
    'Book_1' : {'title': 'Title' , 'author':'Author'},
    'Book_2' : {'title': 'Title' , 'author':'Author'},
    'Book_3' : {'title': 'Title' , 'author':'Author'},
    'Book_4' : {'title': 'Title' , 'author':'Author'},
}

class genreOB(str , Enum):
    horror = 'Horror'
    scifi = 'Scifi'
    comdy = 'Comedy'

@app.get("/")
async def first():
    return books

@app.get("/{B_name}")
async def select_book(B_name : str ):
    return books[B_name]

@app.get("/JOB/{genre}")
async def Genre(genre: genreOB):
    if genre == genreOB.comdy:
        return {'Genre' : genre}
    if genre == genreOB.scifi:
        return {'Genre': genre}
    if genre == genreOB.horror:
        return {'Genre': genre}

@app.get("/books/{book_id}")
async def Book_Id(book_id:int):
    return {'Book ID' : book_id}

@app.post("/")
async def add_book(title ,author):
    count = 0
    if len(books) > 0:
        for book in books:
            x = int(book.split('_')[-1])
            if x > count:
                count = x

    books[f'boook{count + 1}'] = {'title' : title ,'author' : author}
    return book[f'book_{count +1}']

@app.put("/{name}")
async def update(name : str,title : str,author : str):
    information = {'title': title,'author': author}
    books[name] = information
    return information

@app.delete("/{name}")
async def delete_book(name : str):
    del books[name]
    return books

