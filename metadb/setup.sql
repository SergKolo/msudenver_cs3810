-- #############################
-- Setup script for metadb database.
-- Creates tables and related triggers
-- #############################

-- SQLite does not have foreign keys enabled by default
PRAGMA foreign_keys = ON;
-- #############################
-- ENTITY TABLES
-- file table is the parent entity and contains
-- common information which all files should have.
-- Although we could use inode as primary key,
-- this would go against how filesystems expose
-- files to users themselves, so breaks consistency
DROP TABLE IF EXISTS file;
CREATE TABLE file (
    -- primary key already implies not null
    f_path TEXT PRIMARY KEY,
    inode INT,
    size INT,
    ftype_major TEXT,
    ftype_minor TEXT,
    sha256sum TEXT,
    default_app TEXT
);
DROP TABLE IF EXISTS text;
CREATE TABLE text (
    f_path TEXT PRIMARY KEY,
    ftype_minor TEXT,
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

-- utility tables for updating database
DROP TABLE IF EXISTS new_files;
CREATE TABLE new_files AS SELECT * FROM file;
DROP TABLE IF EXISTS changed_files;
CREATE TABLE changed_files AS SELECT * FROM file;

-- #############################
-- TRIGGERS
-- Since SQLite does not allow if statements in triggers - only single WHEN condition,
-- we need conditional trigger to toss each metadata into appropriate table
-- for each table/subtype

CREATE TRIGGER insert_text AFTER INSERT ON file
WHEN new.ftype_major = 'text'
BEGIN
    INSERT INTO text VALUES (new.f_path,new.ftype_minor,
                             get_metadata(new.f_path,new.ftype_major,new.ftype_minor) );
END;

CREATE TRIGGER insert_audio AFTER INSERT ON file
WHEN new.ftype_major = 'audio'
BEGIN

    INSERT INTO audio VALUES (new.f_path,new.ftype_minor,
                             get_metadata(new.f_path,new.ftype_major,new.ftype_minor) );
END;
--CREATE TRIGGER insert_video AFTER INSERT ON file
--WHEN new.ftype_major = 'video'
--BEGIN
--    INSERT INTO video VALUES (new.inode,get_metadata(new.f_path));
--END;
CREATE TRIGGER insert_image AFTER INSERT ON file
WHEN new.ftype_major = 'image'
BEGIN
    INSERT INTO image VALUES (new.f_path,new.ftype_minor,
                             get_metadata(new.f_path,new.ftype_major,new.ftype_minor) );
END;
--CREATE TRIGGER insert_app AFTER INSERT ON file
--WHEN new.ftype_major = 'application'
--BEGIN
--    INSERT INTO application VALUES (new.inode,get_metadata(new.f_path));
--END;
--/* CREATE TRIGGER insert_inode AFTER INSERT ON file
--WHEN new.ftype_major = 'inode'
--BEGIN
--    INSERT INTO inode VALUES (new.inode,count_chars(new.f_path));
--END;
--*/

-- #################################
-- DELETION TRIGGERS 
-- Same idea as before - we need trigger for each type
CREATE TRIGGER delete_text AFTER DELETE ON file
WHEN OLD.ftype_major = 'text'
BEGIN
    DELETE FROM text WHERE OLD.f_path = text.f_path;
END;

CREATE TRIGGER delete_image AFTER DELETE ON file
WHEN OLD.ftype_major = 'image'
BEGIN
    DELETE FROM image WHERE OLD.f_path = image.f_path;
END;

CREATE TRIGGER delete_audio AFTER DELETE ON file
WHEN OLD.ftype_major = 'audio'
BEGIN
    DELETE FROM audio WHERE OLD.f_path = image.f_path;
END;
