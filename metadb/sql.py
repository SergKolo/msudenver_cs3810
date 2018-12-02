# -*- UTF-8 -*-
import sqlite3,os,sys
import re
from time import time
from hashlib import md5
from metadata import *

db_file = os.path.join( os.environ['HOME'],
                        '.config','metadb.sqlite') 

# this may be better than simple_query()
def runsql(func):
    def wrapper(*w_args,**w_kwargs):
        global db_file
        #print("WRAPPER ARGS:",*w_args)
        # string returned from original 'func' goes here
        query_dict = func(*w_args,**w_kwargs)
        try:
            conn = sqlite3.connect(db_file)
        except sqlite.Error as sqlerr:
            # TODO: write a custom function for this
            print(sys.argv[0],
              "Could not open the database file:{0}".format(sqlerr))

        c = conn.cursor()
        #print("QUERY:",query,type(query))
        # For some reason because we need that function for triggers
        # it has to be here on initialization
        if query_dict['func']:
            sqlite3.enable_callback_tracebacks(True)
            conn.create_function(*query_dict['func'])
        # print(query_dict['query'],"\nW_ARGS:",*w_args,len(w_args)) 
        c.execute(query_dict['query'],query_dict['args'])
        return c.fetchall()
        # return conn.commit()
    return wrapper

@runsql
def vacuum():
    print("::DEBUG vacuum")
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

    # File path missing -> delete
    # hash sum changed  -> update
    # type mismatch -> update ?
    # import new files ?
 

    
    pass
        

def load_db():

    @runsql
    def insert_files( value ):
        return { 'query': """ INSERT INTO file VALUES (?,?,?,?,?,?,?)""",
                 'args': value,
                 'func':  tuple([ "get_metadata", 3 , get_metadata])
               }

    if not os.path.exists(db_file):
        init_db()

    for i in walk_home_tree():
        insert_files(i)

def regexp(y,x):
    return True if re.search(y,x)  else False


def find_file(pattern):

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
    if matched_files:
        for i in matched_files:
            print(query_full_info(*i))
            
        

#    # keep it simple, no need to worry about complex db file name
#    db_dir = os.path.join( os.environ['HOME'],'.config','metadb' ) 
#    db_path = os.path.join(db_dir,'metadb')
#
#    try:
#        conn = sqlite3.connect(db_path)
#    except sqlite3.Error as sqlerr:
#        print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))
#
#    c = conn.cursor()
#
#    # setup the database structure
#    with open(  os.path.join( sys.path[0], 'setup.sql' ) ) as setupfile:
#        script = setupfile.realines()    
#        c.execute(query)
#        conn.commit()
#
#    # insert data into files table here
#
#    conn.close()


    #for i in walk_home_tree():

#        query="""
#            INSERT INTO files VALUES(:path,:hash,:gio_type)
#        """
#        c.execute(query,{'path':i[0],'hash':i[1],'gio_type':i[2]})
#
#    conn.commit()
#    query="""
#        SELECT COUNT(*)
#        FROM files;
#    """
#    c.execute(query)
#    # fetch all returns list of tuples
#    # Here, there's just one tuple on list, one item in tuple
#    print(c.fetchall()[0][0]," files imported")
#    conn.close()



# vim: syntax=python:
