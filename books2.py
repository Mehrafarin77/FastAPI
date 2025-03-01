from fastapi import FastAPI, Path, Query, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class BookRequest(BaseModel):
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating:int = Field(gt=0, lt=6)
    published_date:int = Field(lt=2026)

    # to have prefilled fields
    model_config = {
        'json_schema_extra':{
            'example': {
                'title': 'Harry Potter and ...',
                'author': 'Matthew Perry',
                'description': 'Some description ...',
                'rating': 4,
                'published_date': 2020
            }
        }
    }

class Book:
    def __init__(self, title: str, author:str, description: str, rating:int, published_date: int, id:int = 0):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


books = [
    Book('Harry Potter 1', 'j.k.rowling', 'first hp book', 4, 2012,1),
    Book('Harry Potter 2', 'j.k.rowling', 'second hp book', 4, 2013,2),
    Book('Harry Potter 3', 'j.k.rowling', 'third hp book', 5, 2014, 3),
    Book('Harry Potter 4', 'j.k.rowling', 'fourth hp book', 5, 2015,4)
]


@app.get('/books')
def get_books():
    return books

@app.post('/books/new', status_code = 201)
def add_book(new_book: BookRequest):
    book = Book(**new_book.dict())
    book.id = len(books) + 1
    books.append(book)
    return new_book


@app.get('/books/by_rating')
def get_book_by_rating(rating: int = Query(gt=0, lt=6)):
    result_books = []
    for book in books:
        if book.rating == rating:
            result_books.append(book)
    if not result_books:
        raise HTTPException(status_code=404,
                            detail= f'No book with rating: {rating} found.')
    return result_books

@app.get('/books/by_published_date')
def get_book_by_year(date: int = Query(lt=2026)):
    result_books = []
    for book in books:
        if book.published_date == date:
            result_books.append(book)
    if not result_books:
        raise HTTPException(status_code=404,
                            detail= f'No book with published year: {date} found.')
    return result_books


@app.get('/books/{id}')
def get_book(id: int = Path(gt=0)):    # Path() is used when we want to validate a parameter
    for book in books:
        if book.id == id:
            return book

    raise HTTPException(status_code=404,
                        detail= f'No book with id: {id} found.')


@app.put('/books/update/{id}', status_code = 201)
def update_book(updated_book: BookRequest, id: int = Path(gt=0)):
    found = False
    for i in range(len(books)):
        if books[i].id == id:
            books[i] = Book(**updated_book.dict())
            books[i].id = id
            found = True

    if not found:
        raise HTTPException(status_code=404,
                            detail= f'No book with id: {id} found.')
    return updated_book

@app.delete('/books/delete/{id}', status_code = 204)
def delete_book(id: int = Path(gt=0)):
    found = False
    for book in books:
        if book.id == id:
            books.remove(book)
            found = True

    if not found:
        raise HTTPException(status_code=404,
                            detail= f'No book with id: {id} found.')
    return 'Book deleted successfully.'