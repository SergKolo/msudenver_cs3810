#!/usr/bin/env python3
import os
from sql import init_database

def first_run():
    user_home = os.environ['HOME']
    config_dir = os.path.join(user_home,'.config','metadb')
    if not os.path.exists(config_dir):
        # TODO: mode rwx for user, but no-one else
        os.makedirs(config_dir)
    # TODO: checking for existing db
    init_database(config_dir)
   

def main():
    first_run()

if __name__ == '__main__':
    main()
