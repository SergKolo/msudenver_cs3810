# -*- UTF-8 -*-
import sqlite3, os,sys
from time import time
from hashlib import md5
from metadata import walk_home_tree

# we're repeating ourselves too much
# Should config_dir be made global ?
def simple_query(config_dir,query):
    db_filter = filter(lambda x: x.endswith('.db'),os.listdir(config_dir))
    db_fname = list(db_filter)[0]
    db_path = os.path.join(config_dir,db_fname)
    
    try:
        conn = sqlite3.connect(db_path)
    except sqlite.Error as sqlerr:
        print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))

    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

def dump_all(config_dir):
    query="""SELECT * FROM files"""
    return simple_query(config_dir,query)

def updatedb():

    # File path missing -> delete
    # hash sum changed  -> update
    # type mismatch -> update ?
    # import new files ?

    #    db_filter = filter(lambda x: x.endswith('.db'),os.listdir(config_dir))
    #    db_fname = list(db_filter)[0]
    #    db_path = os.path.join(config_dir,db_fname)
    #
    #    try:
    #        conn = sqlite3.connect(db_path)
    #    except sqlite.Error as sqlerr:
    #        print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))
    #
    #    c = conn.cursor()
    #    for i in 
    
    pass
        

def init_database(config_dir):

    for f in os.listdir(config_dir):
        os.unlink(os.path.join(config_dir,f))

    db_name = ''.join([os.environ['USER'],str(time())])  
    db_hash = md5()
    db_hash.update(db_name.encode())
    db_fname = ''.join([db_hash.hexdigest(),'.db'])
    db_path = os.path.join(config_dir,db_fname)
    # print(":::DEBUG:",db_path)


    try:
        conn = sqlite3.connect(db_path)
    except sqlite.Error as sqlerr:
        print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))
    c = conn.cursor()

    query="""
        CREATE TABLE IF NOT EXISTS files (
            f_path TEXT, hash TEXT, gio_filetype INT
        )
    """
    c.execute(query)
    conn.commit()


    # TODO: do we pass $HOME here or in metadata.py ?
    for i in walk_home_tree():
        #print("::DEBUG:",i) 
        query="""
            INSERT INTO files VALUES(:path,:hash,:gio_type)
        """
        c.execute(query,{'path':i[0],'hash':i[1],'gio_type':i[2]})

    conn.commit()
    query="""
        SELECT COUNT(*)
        FROM files;
    """
    c.execute(query)
    # fetch all returns list of tuples
    # Here, there's just one tuple on list, one item in tuple
    print(c.fetchall()[0][0]," files imported")
    conn.close()
