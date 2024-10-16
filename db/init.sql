DROP TABLE IF EXISTS messages;

CREATE TABLE IF NOT EXISTS messages(
    id serial PRIMARY KEY,
    title text NOT NULL,
    body text NOT NULL
);

INSERT INTO messages (title, body) VALUES ('Initial Message', 'Hello, World!');