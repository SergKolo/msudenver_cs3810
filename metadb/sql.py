# -*- UTF-8 -*-
import sqlite3,os,sys
import re
import pprint
from time import time
from hashlib import md5
from metadata import *

""" This module is intended for working with SQLite database.
    runsql decorator is used to perform queries in a simple and
    consistent manner. Instead of opening database each and every 
    time we run query, this is already done with the decorator.
"""


db_file = os.path.join( os.environ['HOME'],
                        '.config','metadb.sqlite') 

def runsql(func):
    ''' Decorator for easy sqlite queries. Decorated function
        must return a dictionary consisting of 3 items:
        query - string of SQL statements to be executed, 
        args - tuple of arguments to parametrized queries, 
        func - user-defined function used within query or related
        triggers '''
    def wrapper(*w_args,**w_kwargs):
        global db_file
        query_dict = func(*w_args,**w_kwargs)
        try:
            conn = sqlite3.connect(db_file)
        except sqlite.Error as sqlerr:
            # TODO: write a custom function for this
            print(sys.argv[0],
              "Could not open the database file:{0}".format(sqlerr))
            exit(2)
        c = conn.cursor()
        if query_dict['func']:
            sqlite3.enable_callback_tracebacks(True)
            conn.create_function(*query_dict['func'])
        c.execute(query_dict['query'],query_dict['args'])
        if query_dict['query'].lstrip().upper().startswith("SELECT"):
            return c.fetchall()
        return conn.commit()
    return wrapper

@runsql
def vacuum():
    return { 'query': """ DELETE FROM file WHERE file_exists(file.f_path) = 0 """,
	     'args': None,
	     'func':  tuple([ "file_exists", 1 , lambda x: 1 if os.path.exists(x) else 0 ])
    }
        

def init_db():
    global db_file
    # The database file doesn't exist.
    # Create database file with all basic tables
    with open(os.path.join(sys.path[0],'setup.sql')) as setup:
        try:
    	    conn = sqlite3.connect(db_file)
        except sqlite3.Error as sqliterr:
    	    print("SQLite error: {0}".format(sqliterr))
    	    sys.exit(2)
        curs = conn.cursor()
        script = setup.read()
        curs.executescript(script)
        conn.commit()
        conn.close()

def updatedb():
    pass
        

def load_db():

    @runsql
    def insert_files( value ):
        # value arg should already be tuple
        return { 'query': """ INSERT INTO file VALUES (?,?,?,?,?,?,?)""",
                 'args': value,
                 'func':  tuple([ "get_metadata", 3 , get_metadata])
               }

    if not os.path.exists(db_file):
        init_db()

    for i in walk_home_tree():
        insert_files(i)

def regexp(y,x):
    """ Used to implement REGEXP function for SQLite, 
        see https://www.sqlite.org/lang_expr.html """
    return True if re.search(y,x)  else False


def find_file(pattern):
    ''' Returns all information in parent table plus
        information specific to the file in pretty print format'''
    @runsql
    def get_file_and_subtype(pattern):
        return { 'query': """ SELECT f_path,ftype_major FROM file 
                              WHERE f_path REGEXP ? """,
                 'args': (pattern, ),
                 'func': tuple(["REGEXP",2,regexp])
               }    

    @runsql
    def query_full_info(fpath,table):
        return { 'query': """ SELECT * FROM file 
                              JOIN {0} ON file.f_path = {0}.f_path 
                              AND file.f_path = ?""".format(table),
                 'args': (fpath, ),
                 'func': None
               }

    matched_files = get_file_and_subtype(pattern)
    pp = pprint.PrettyPrinter(indent=4)
    if matched_files:
        for i in matched_files:
            result = query_full_info(*i)
            if result:
                newresult = list(result[0])
                newresult.pop(7)
                pp.pprint(newresult)

# vim: syntax=python:
