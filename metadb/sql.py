# -*- UTF-8 -*-
import sqlite3, os
from time import time
from hashlib import md5
from metadata import walk_home_tree

# we're repeating ourselves too much
# Should config_dir be made global ?
def simple_query(config_dir,query):
    db_filter = filter(lambda x: x.endswith('.db'),os.listdir(config_dir))
    db_fname = list(db_filter)[0]
    db_path = os.path.join(config_dir,db_fname)

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()

def init_database(config_dir):
    db_name = ''.join([os.environ['USER'],str(time())])  
    db_hash = md5()
    db_hash.update(db_name.encode())
    db_fname = ''.join([db_hash.hexdigest(),'.db'])
    db_path = os.path.join(config_dir,db_fname)
    print(":::DEBUG:",db_path)


    conn = sqlite3.connect(db_path)
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
        print("::DEBUG:",i) 
        query="""
            INSERT INTO files VALUES(:path,:hash,:gio_type)
        """
        c.execute(query,{'path':i[0],'hash':i[1],'gio_type':i[2]})

    conn.commit()
    conn.close()
