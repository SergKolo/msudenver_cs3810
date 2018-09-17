#!/usr/bin/env python3
import os,argparse
from sql import *

def first_run(config_dir):
    if not os.path.exists(config_dir):
        # TODO: mode rwx for user, but no-one else
        os.makedirs(config_dir)
    # TODO: checking for existing db
    init_database(config_dir)
   

def parse_cmd_args():

    # TODO: https://stackoverflow.com/a/11155124/3701431
    # TODO: how do we handle --metadata arg ?
    desc = """Database for files in user's home directory
              Authors: Sergiy Kolodyazhnyy
                       Liu Tian
           """
    argp = argparse.ArgumentParser(desc)

    argp.add_argument(
        "-d","--dump",
        action='store_true'
    )
    argp.add_argument(
         "-i","--init",
         action='store_true'
    )
    argp.add_argument(
        "-t","--type-query",
        action='store',
        type=str
    )
    argp.add_argument(
        "-m","--metadata",
        action='store',
        type=str
    )
    return argp.parse_args()


def main():

    args = parse_cmd_args()

    user_home = os.environ['HOME']
    config_dir = os.path.join(user_home,'.config','metadb')
    conf_files = filter(lambda x: x.endswith('.db'), os.listdir(config_dir) )

    # TODO: should we run first_run() automatically or 
    # follow user's arguments ?
    #if len(list(conf_files)) == 0:

    if args.init:
        first_run(config_dir)
    if args.dump:
        print(dump_all(config_dir))
    
#    query = """SELECT * 
#               FROM files 
#               WHERE gio_filetype LIKE 'application/%'"""
#    result = simple_query(config_dir,query)
#    print(result)

if __name__ == '__main__':
    main()
