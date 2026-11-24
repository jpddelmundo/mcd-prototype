import pandas as pd
import pymysql
from pathlib import Path
from sqlalchemy import create_engine

METADATA_PATH = Path("assets/metadata")

engine = create_engine("mysql+pymysql://root:admin@localhost:3306/mcd")

metadataDf = pd.read_json(f"{METADATA_PATH / 'all-metadata.json'}")
booksDf = pd.read_json("book_catalogue.json")
# print(metadataDf.head(10))
# print(booksDf.head(10))

joinedDf = booksDf.join(metadataDf.set_index("isbn"), on="isbn", how="inner", lsuffix="_l", rsuffix="_r")


with engine.connect() as connection:
    for col in joinedDf.columns:
        if joinedDf[col].dtype == "object":
            joinedDf[col] = joinedDf[col].astype(str)

    joinedDf = joinedDf[["isbn", "title", "publisher", "author", "short_description",
                         "long_description", "copyright", "edition", "no_of_pages",
                         "keywords", "references", "article"]]
    
    print(joinedDf[["isbn", "title"]])

    joinedDf.to_sql(name="books", con=connection, if_exists="replace", index=False)