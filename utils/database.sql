CREATE TABLE encoding (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    encoding BLOB NOT NULL
);