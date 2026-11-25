from typing import Annotated

from fastapi import FastAPI, Depends, Query
from sqlalchemy import select, MetaData, Table, or_
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URI = "mysql+pymysql://root:admin@host.docker.internal:3306/mcd"
metadata = MetaData()
engine = create_engine(url=DATABASE_URI)

# Reflect all existing tables from the MySQL database
# Access mapped classes by their exact MySQL tables names
books = Table("books", metadata, autoload_with=engine)

def get_db():
    with Session(engine) as session:
        yield books

SessionDep = Annotated[Session, Depends(get_db)]

@app.get("/index")
async def helloworld():
    return {"message": "Hello World"}

@app.get("/books/v1")
async def get_books(
    db: SessionDep,
    keyword: Annotated[str | None, Query(max_length=50)] = None):
    regex_pattern = "^[a-zA-Z0-9[^a-zA-Z0-9]]?"+"+" \
        .join([char for char in keyword])+"?[a-zA-Z0-9[^a-zA-Z0-9]]?"
    if keyword:
        books2 = db.execute(select(books)
            .where(
                or_(
                    books.c.isbn.regexp_match(regex_pattern),
                    books.c.title.regexp_match(regex_pattern),
                    books.c.keywords.regexp_match(regex_pattern),
                    books.c.long_description.regexp_match(regex_pattern),
                    books.c.short_description.regexp_match(regex_pattern),
                    books.c.publisher.regexp_match(regex_pattern),
                    books.c.author.regexp_match(regex_pattern),
                    books.c.references.regexp_match(regex_pattern)
                    )
                )
            ).mappings().all()
        return books2