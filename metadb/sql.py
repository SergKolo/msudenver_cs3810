# -*- UTF-8 -*-
import sqlite3, os,sys
from time import time
from hashlib import md5
from metadata import walk_home_tree

db_file = os.path.join( os.environ['HOME'],'.config','metadb.sqlite') 

# this may be better than simple_query()
def runsql(func):
    def wrapper(*args,**kwargs):
        global db_file
        query = func(*args,**kwargs)
        print('>>> QUERY:',query[0],query[1])

        try:
            conn = sqlite3.connect(db_file)
        except sqlite.Error as sqlerr:
            # TODO: write a custom function for this
            print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))

        c = conn.cursor()
        c.execute(str(query[0]),(query[1],))
        return c.fetchall()
    return wrapper
    

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
        #print(script)
        curs.executescript( script)
        conn.commit()
        conn.close()

def updatedb():

    # File path missing -> delete
    # hash sum changed  -> update
    # type mismatch -> update ?
    # import new files ?
 

    
    pass
        

def load_db():

    if not os.path.exists(db_file):
        init_db()

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
