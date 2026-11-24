from fastapi import FastAPI
from sqlalchemy import select, MetaData, Table
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

query = None
resp = []
with Session(engine) as session:
    books2 = session.execute(select(books).limit(5)).all()
    for book in books2:
        print(book)