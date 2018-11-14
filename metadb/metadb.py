#!/usr/bin/env python3
import os,argparse
from sql import *

def parse_cmd_args():

    # TODO: https://stackoverflow.com/a/11155124/3701431
    # TODO: how do we handle --metadata arg ?
    desc = """Database for files in user's home directory
              Authors: Sergiy Kolodyazhnyy, Liu Tian
           """
    argp = argparse.ArgumentParser(desc)

    argp.add_argument(
        "-d","--dump",
        action='store_true'
    )

    argp.add_argument(
        "-e","--exists",
        action='store_true'
    )
    argp.add_argument(
         "-i","--init",
         action='store_true'
    )
    argp.add_argument(
        "-t","--type",
        action='store',
        type=str
    )
    argp.add_argument(
        "-m","--metadata",
        action='store',
        type=str
    )

    argp.add_argument(
        "-u","--update",
        action='store_true'
    )
    return argp.parse_args()


def main():

    args = parse_cmd_args()

    if args.init:
        first_run(config_dir)

    if args.dump:
        for i in dump_all(config_dir):
            fmtstr="Path:{0}\nSHA256:{1}\nType:{2}".format(*i)
            if args.exists:
                extrastr="".join(["Exists:", str(os.path.exists(i[0]))] )
                fmtstr="\n".join([fmtstr,extrastr])
            print(fmtstr,"\n")

    if args.type:
        print('>>> ARGS.TYPE',args.type)
        
        @runsql
        def get_types(type):
            return  ( """ SELECT * 
                          FROM files 
                          WHERE gio_filetype LIKE ? """, "/".join([type,"%"]))

        for i in get_types(args.type):
            print("Path:{0}\nSHA256:{1}\nType:{2}\n".format(*i))

    if args.update:
        updatedb()
    
#    query = """SELECT * 
#               FROM files 
#               WHERE gio_filetype LIKE 'application/%'"""
#    result = simple_query(config_dir,query)
#    print(result)

if __name__ == '__main__':
    main()
