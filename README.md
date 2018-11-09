### Meta-DB Database Requirements
Authors:
- Tian Liu
- Sergiy Kolodyazhnyy
- Jericha Bradley

## Contents
1. Introduction
   1. Purpose and Objectives
   2. Assumptions and Dependencies
2. Architecture
    1. Overview of the Database Architecture
    2. Software Dependencies
    3. Hardware Dependencies
    4. Limitations and Constraints
3. Database Model
    1. Overview of Entities
    2. Required Tables
4. Database-User Interfacing
    1. Information Flow
    2. Common User Queries

## 1. Introduction
### 1.1 Purpose and Objectives

The goals of this application:
- to provide a convenient way for users to search for files based on particular metadata
- to provide a convenient way for users to show metadata of specific files
- to provide a more powerful alternative to the standard locatedb on Linux/Unix systems

The application aims at desktop use, however the application suits well for server environment as well. In such environments as file storage/archiving or file sharing service the application provides means to locate particular file on a more fine-grained sets of requirements. In the image/audio processing environment where multiple files and encoding types frequently have to coexist, the application can provide means of better control over indexing the processed data. The application can be used as standalone command as well as in scripting applications, where information written to stdout stream may be redirected to other applications via standard unix pipelines or temporary files.

### 1.2 Assumptions and Dependencies
## 2. Architecture
### 2.1 Overview of the Database Architecture
### 2.2 Software Dependencies

Primary software used in this application:
- SQLite 3
- Python 3

Since the SQLite is intended for data aggregation and incapable of implementing system functions needed for the data discovery, such as traversing the directory tree for each user directory or discovering metadata for particular file, the bulk of the job is done by Python 3 modules. In particular, the following modules are necessary:

- `PIL` for image metadata discovery

In order to process metadata of the files

### 2.3 Hardware Dependencies

~~In order for the application to function in average desktop-use environment, it is not necessary~~

If the application will be used within server environment where performance might matter, the database may be ran from RAM, which requires sufficient amount of RAM to hold all indexes. SQLite is limited to size of 140 Terabytes ( 2<sup>47</sup> bytes).  

### 2.4 Limitations and Constraints

The choice of the database software for this project influences the constraints on how SQL code will be structured. For instance, SQLite does not support conditional triggers. However, it is possible to implement conditional trigger via multiple triggers that fire when single specific condition is met. For instance, where in MySQL we could do

```SQL
CREATE TRIGGER record_type AFTER INSERT ON file
FOR EACH ROW BEGIN
    IF (New.filetype = 'text') THEN
        INSERT INTO text_file (path) VALUES ( New.path );
    ELSE IF (New.filetype = 'image') THEN
        INSERT INTO image_file (path) VALUES  (New.path);
    END IF;
END;
```

in SQL we will have to split this into two triggers as so

```SQL
    CREATE TRIGGER record_text AFTER INSERT ON file
    WHEN New.filetype = 'text'
    BEGIN
        INSERT INTO text_file   (path) VALUES (New.path);
    END;

    CREATE TRIGGER record_image AFTER INSERT ON file
    WHEN New.filetype = 'text'
    BEGIN
        INSERT INTO image_file (path) VALUES (New.path);
    END;

```




## 3. Database Model

The database models files and relation with their metadata via inheritance model. All objects that are discovered by the application via traversal of the  user's directories are going to be files, but each file has particular 'is a' relationship with major filetype.  

Natural key to uniquely identify a file is pathname.

### 3.1 Overview of Entities
### 3.2 Required Tables
## 4. Database-User Interfacing



### 4.1 Information Flow
### 4.2 Common User Queries
