-- since this script is intended for initial setup, there's no need to 
-- drop tables nor triggers. All custom functions should be defined before
-- this script runs

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS file;
CREATE TABLE file (
    -- primary key already implies not null
    f_path TEXT PRIMARY KEY,
    inode INT,
    size INT,
    ftype_major TEXT,
    sha256sum TEXT,
    default_app TEXT
);
DROP TABLE IF EXISTS text;
CREATE TABLE text (
    f_path TEXT PRIMARY KEY,
    fftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);

DROP TABLE IF EXISTS application;
CREATE TABLE application (
    f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);
DROP TABLE IF EXISTS image;
CREATE TABLE image (
   f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);
DROP TABLE IF EXISTS video;
CREATE TABLE video (
   f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);
DROP TABLE IF EXISTS audio;
CREATE TABLE audio (
   f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);
-- DROP TABLE IF EXISTS inode;
/* CREATE TABLE inode (
   f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
    metadata TEXT,
    FOREIGN KEY (f_path) REFERENCES file(f_path)
);
*/
-- utility tables for updating database
DROP TABLE IF EXISTS new_files;
CREATE TABLE new_files AS SELECT * FROM file;
DROP TABLE IF EXISTS changed_files;
CREATE TABLE changed_files AS SELECT * FROM file;

-- we need conditional trigger to toss each metadata into appropriate table
-- for each table/subtype

CREATE TRIGGER insert_text AFTER INSERT ON file
WHEN new.ftype_major = 'text'
BEGIN
    INSERT INTO text VALUES (new.path,get_minor(new.path),get_metadata(f_path,new.major));
END;

CREATE TRIGGER insert_audio AFTER INSERT ON file
WHEN new.ftype_major = 'audio'
BEGIN
    INSERT INTO audio VALUES (new.inode,get_metadata(new.f_path));
END;
CREATE TRIGGER insert_video AFTER INSERT ON file
WHEN new.ftype_major = 'video'
BEGIN
    INSERT INTO video VALUES (new.inode,get_metadata(new.f_path));
END;
CREATE TRIGGER insert_image AFTER INSERT ON file
WHEN new.ftype_major = 'image'
BEGIN
    INSERT INTO image VALUES (new.inode,get_metadata(new.f_path));
END;
CREATE TRIGGER insert_app AFTER INSERT ON file
WHEN new.ftype_major = 'application'
BEGIN
    INSERT INTO application VALUES (new.inode,get_metadata(new.f_path));
END;
/* CREATE TRIGGER insert_inode AFTER INSERT ON file
WHEN new.ftype_major = 'inode'
BEGIN
    INSERT INTO inode VALUES (new.inode,count_chars(new.f_path));
END;
*/
