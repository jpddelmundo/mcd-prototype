from fastapi import FastAPI
from sqlalchemy import select, MetaData, Table, or_
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URI = "mysql+pymysql://root:admin@localhost:3306/mcd"
metadata = MetaData()
engine = create_engine(url=DATABASE_URI)

# Reflect all existing tables from the MySQL database
# Access mapped classes by their exact MySQL tables names
books = Table("books", metadata, autoload_with=engine)


@app.get("/books/v1")
async def get_books(keyword: str | None = None):
    resp = []
    regex_pattern = "^[a-zA-Z0-9]?"+"+".join([char for char in keyword])+"?"
    if keyword:
        with Session(engine) as session:
            books2 = session.execute(select(books)
                                     .where(or_(books.c.isbn.regexp_match(regex_pattern),
                                            books.c.title.regexp_match(regex_pattern),
                                            books.c.keywords.regexp_match(regex_pattern),
                                            books.c.long_description.regexp_match(regex_pattern),
                                            books.c.short_description.regexp_match(regex_pattern),
                                            books.c.publisher.regexp_match(regex_pattern),
                                            books.c.author.regexp_match(regex_pattern),
                                            books.c.references.regexp_match(regex_pattern)))).all()
            for book in books2:
                obj = {"isbn": book[0], "title": book[1], "publisher": book[2],
                   "author": book[3], "short_description": book[4],
                    "long_description": book[5], "copyright": book[6],
                    "edition": book[7], "no_of_pages": book[8],
                    "references": book[9], "keywords": book[10],
                    "article": book[11]}
                resp.append(obj)
        return resp