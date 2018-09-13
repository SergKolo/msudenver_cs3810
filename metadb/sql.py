# -*- UTF-8 -*-
import sqlite3, os
from time import time
from hashlib import md5
from metadata import walk_home_tree

def init_database(config_dir):
    db_name = ''.join([os.environ['USER'],str(time())])  
    db_hash = md5()
    db_hash.update(db_name.encode())
    db_path = os.path.join(config_dir,db_hash.hexdigest())
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
