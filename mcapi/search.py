import sys
import json
import pymysql

connstring = {"host": "localhost",
              "user": "root",
              "password": "admin",
              "port": 3306,
              "database": "mcd"}

keyword = sys.argv[1]
regex_pattern = "^"+"+".join([char for char in keyword])+"?"

with pymysql.connect(**connstring) as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM mcd.books LIMIT 0")
        columns = [d[0] for d in cursor.description]
        print(columns)

        where_predicates = " OR ".join([f"REGEXP_LIKE (`{col}`, {repr(regex_pattern)})" 
                                        for col in columns])
        query = f"SELECT * FROM mcd.books WHERE {where_predicates}"
        cursor.execute(query)
        res3 = cursor.fetchall()
        for row in res3:
            print(json.dumps({"isbn": row[0],
                   "title": row[1],
                   "publisher": row[2],
                   "author": row[3],
                    "short_description": row[4],
                    "long_description": row[5],
                    "copyright": row[6],
                    "edition": row[7],
                    "no_of_pages": row[8],
                    "references": row[9],
                    "keywords": row[10],
                    "article": row[11]}, indent=2), end=",\n")