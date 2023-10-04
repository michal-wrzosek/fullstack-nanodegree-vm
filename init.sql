-- Create the "news" database
CREATE DATABASE news;

-- Switch to the "news" database
\c news;

-- Create the "forum" database
CREATE DATABASE forum;

-- Switch to the "forum" database
\c forum;

-- Create a table called "posts" in the "forum" database
CREATE TABLE posts (
    content TEXT,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id SERIAL
);
