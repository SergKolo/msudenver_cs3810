# -*- UTF-8 -*-
import sqlite3, os,sys
from time import time
from hashlib import md5
from metadata import walk_home_tree

# this may be better than simple_query()
def runsql(func):
    #print(">>>RUNSQL:",args)
    def wrapper(*args,**kwargs):
        print(args)
        db_dir = os.path.join(os.environ['HOME'],'.config','metadb')
        db_filter = filter(lambda x: x.endswith('.db'),
                           os.listdir(db_dir))
        db_fname = list(db_filter)[0]
        db_path = os.path.join(db_dir,db_fname)

        query = func(*args,**kwargs)
        print('>>> QUERY:',query[0],query[1])

        try:
            conn = sqlite3.connect(db_path)
        except sqlite.Error as sqlerr:
            print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))

        c = conn.cursor()
        c.execute(str(query[0]),(query[1],))
        return c.fetchall()
    return wrapper
    

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
        

def load_db():

    # keep it simple, no need to worry about complex db file name
    db_dir = os.path.join( os.environ['HOME'],'.config','metadb' ) 
    db_path = os.path.join(db_dir,'metadb')

    try:
        conn = sqlite3.connect(db_path)
    except sqlite.Error as sqlerr:
        print(sys.argv[0],"Could not open the database file:{0}".format(sqlerr))

    c = conn.cursor()

    # setup the database structure
    with open(  os.path.join( sys.path[0], 'setup.sql' ) as setupfile:
        script = setupfile.realines()    
        c.execute(query)
        conn.commit()

    # insert data into files table here

    conn.close()


#    # TODO: do we pass $HOME here or in metadata.py ?
#    for i in walk_home_tree():
#        #print("::DEBUG:",i) 
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
