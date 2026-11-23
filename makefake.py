import json
import random
from pathlib import Path

from faker import Faker
from faker.providers import person

SEED = 8746
METADATA_PATH = Path("assets/metadata")

faker = Faker()
Faker.seed(SEED)
rand = random.Random(SEED)

books = {}
books["records"] = []
categories = [""]

def fake_authors():
    authors = []
    for _ in range(rand.randint(1, 3)):
        authors.append({"name": faker.name(),
                        "address": faker.address(),
                        "contact_no": faker.phone_number(),
                        "email": faker.email()})
    return authors

def fake_publishers():
    publishers = []
    for _ in range(rand.randint(1, 3)):
        publishers.append({"name": faker.name(),
                        "address": faker.address(),
                        "contact_no": faker.phone_number(),
                        "email": faker.email()})
    return publishers

def fake_metadata(isbn: str, **kwargs) -> list:
    rand = random.Random(isbn)
    return [
        {"isbn": isbn,
         "title": kwargs["title"], 
        "keywords": [faker.word() for kw in range(rand.randint(20, 30))],
         "references": [faker.name() 
                        + " (" + faker.year() + "), " 
                        + " ".join([word.title() 
                               for word in faker.sentence().rstrip(".").split(" ")]) 
                               for _ in range(rand.randint(2, 5))],
        "article": faker.paragraph(nb_sentences=20)}]

def main():
    for i in range(1001):
        books["records"].append(
            {"isbn": faker.isbn13(separator=""),
            "title": (" ".join([word.title() for word in faker.sentence().rstrip(".").split(" ")])),
            "publisher": fake_publishers(),
            "short_description": faker.paragraph(nb_sentences=rand.randint(1, 10)),
            "long_description": faker.paragraph(nb_sentences=rand.randint(1, 40)),
            "author": fake_authors(),
            "copyright": int(f"20{rand.randint(1, 26):02}"),
            "edition": rand.randint(1, 4),
            "no_of_pages": rand.randint(200, 700),})

    with open("book_catalogue.json", "w") as f:
        f.write(json.dumps(books["records"], indent=2))

    # read the JSON, and create a fake metadata for each item
    bookCatalogueJson = open("book_catalogue.json", "r")
    book_catalogue_JSON = json.loads(bookCatalogueJson.read())

    # creates the metadata folder if it doesn't exists
    METADATA_PATH.mkdir(exist_ok=True)

    for book in book_catalogue_JSON:
        title_metadata_path = METADATA_PATH / book["title"]
        title_metadata_path.mkdir(parents=True, exist_ok=True)
        markdown_file = title_metadata_path / f"{book['title']}.md"
        json_file = title_metadata_path / f"{book['title']}.json"
        markdown_file.touch(exist_ok=True); json_file.touch(exist_ok=True)
        json_file.write_text(json.dumps(fake_metadata(isbn=book['isbn'], title=book['title']), indent=2))

    bookCatalogueJson.close()


if __name__ == "__main__":
    main()