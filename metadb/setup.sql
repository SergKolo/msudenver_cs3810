-- since this script is intended for initial setup, there's no need to 
-- drop tables nor triggers. All custom functions should be defined before
-- this script runs

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

CREATE TABLE application (
    inode INT,
    char_count INT
);
CREATE TABLE video  (
    inode INT,
    char_count INT
);
CREATE TABLE image (
    inode INT,
    char_count INT
);
CREATE TABLE inode  (
    inode INT,
    char_count INT
);

CREATE TABLE audio (
    inode INT,
    char_count INT
);

CREATE TABLE new_files AS SELECT * FROM file;
CREATE TABLE changed_files AS SELECT * FROM file;

-- we need conditional trigger to toss each metadata into appropriate table
-- for each table/subtype

CREATE TRIGGER insert_text AFTER INSERT ON file
WHEN new.type_major = 'text'
BEGIN
    INSERT INTO text VALUES (new.inode,count_chars(new.f_path));
END

CREATE TRIGGER insert_audio AFTER INSERT ON file
WHEN new.type_major = 'audio'
BEGIN
    INSERT INTO audio VALUES (new.inode,count_chars(new.f_path));
END
CREATE TRIGGER insert_video AFTER INSERT ON file
WHEN new.type_major = 'video'
BEGIN
    INSERT INTO video VALUES (new.inode,count_chars(new.f_path));
END
CREATE TRIGGER insert_image AFTER INSERT ON file
WHEN new.type_major = 'image'
BEGIN
    INSERT INTO image VALUES (new.inode,count_chars(new.f_path));
END
CREATE TRIGGER insert_app AFTER INSERT ON file
WHEN new.type_major = 'application'
BEGIN
    INSERT INTO application VALUES (new.inode,count_chars(new.f_path));
END
CREATE TRIGGER insert_inode AFTER INSERT ON file
WHEN new.type_major = 'inode'
BEGIN
    INSERT INTO inode VALUES (new.inode,count_chars(new.f_path));
END
