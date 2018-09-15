#!/usr/bin/env python3
import os
from sql import *

def first_run(config_dir):
    if not os.path.exists(config_dir):
        # TODO: mode rwx for user, but no-one else
        os.makedirs(config_dir)
    # TODO: checking for existing db
    init_database(config_dir)
   

def main():
    user_home = os.environ['HOME']
    config_dir = os.path.join(user_home,'.config','metadb')
    conf_files = filter(lambda x: x.endswith('.db'), os.listdir(config_dir) )
    if len(list(conf_files)) == 0:
        first_run(config_dir)
    
#    query = """SELECT * 
#               FROM files 
#               WHERE gio_filetype LIKE 'application/%'"""
#    result = simple_query(config_dir,query)
#    print(result)

if __name__ == '__main__':
    main()
