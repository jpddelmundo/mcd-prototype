CREATE TABLE IF NOT EXISTS mcd.books (
    isbn VARCHAR(25),
    title VARCHAR(155),
    publisher JSON,
    short_description VARCHAR(255),
    long_description VARCHAR(500),
    author JSON,
    copyright INTEGER,
    edition TINYINT,
    no_of_pages INTEGER
);