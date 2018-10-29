DROP TABLE IF EXISTS file;
DROP TABLE IF EXISTS text;

CREATE TABLE file (
    f_path TEXT,
    inode INT,
    type_major TEXT,
    type_minor TEXT,
    sha256sum TEXT,
    mtime DATE,
    default_app TEXT
);

CREATE TABLE text(
    inode INT,
    char_count INT
);

CREATE TRIGGER insert_text AFTER INSERT ON file
WHEN new.type_major = 'text'
BEGIN
    INSERT INTO text VALUES (new.inode,count_chars(new.f_path));
END
