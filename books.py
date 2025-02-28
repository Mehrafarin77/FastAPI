from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

books = [
    {'title': 'title one', 'author': 'author one', 'category': 'history'},
    {'title': 'title two', 'author': 'author two', 'category': 'art'},
    {'title': 'title three', 'author': 'author three', 'category': 'biology'},
    {'title': 'title four', 'author': 'author four', 'category': 'math'},
    {'title': 'title five', 'author': 'author five', 'category': 'technology'},
    {'title': 'title six', 'author': 'author five', 'category': 'math'},
]

class Book(BaseModel):
    title: str
    author: str
    category: str

@app.get('/books')
def get_books():
    return books


@app.post('/books/create_book')
def create_book(book: Book):
    books.append(**book.dict())
    return new_book

@app.put('/books/update')
def edit_book(updated_book: Book):
    for i in range(len(books)):
        if books[i].get('title').casefold() == updated_book.title.casefold():
            books[i] = updated_book
    return updated_book

@app.delete('/books/{title}')
def delete_book(title: str):
    for book in books:
        if book.get('title').casefold() == title.casefold():
            books.remove(book)


@app.get('/books/{author}')
def author_books(author: str):
    author_books = []
    for book in books:
        if book.get('author').casefold() == author.casefold():
            author_books.append(book)
    return author_books

