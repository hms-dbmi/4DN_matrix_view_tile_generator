#!/usr//bin/python
import json
from optparse import OptionParser
import os
import sqlite3
import math

__author__ = 'Hendrik Strobelt'


def norm(x, max_v):
    return math.log(x + 1) / max_v


def run(args, options):
    input_file_name = args[0]
    resolution = int(args[1])
    output_dir_name = args[2]
    project_dir = os.path.join(output_dir_name, '_project')
    index_file_name = os.path.join(project_dir, 'index.sqlite')
    config_file_name = os.path.join(project_dir, 'config.json')
    if not os.path.isdir(project_dir):
        os.makedirs(project_dir)

    # create cahce if not exist yet:
    if not os.path.isfile(index_file_name) or options.recache:
        if os.path.isfile(input_file_name):
            conn = sqlite3.connect(index_file_name)
            with conn:
                cur = conn.cursor()
                cur.execute("DROP TABLE IF EXISTS CacheDB")
                cur.execute("CREATE TABLE CacheDB(PosX INT, PosY INT, Value REAL)")
                i = 0
                max_pos = 0
                max_value = 0
                with open(input_file_name) as input_file:
                    for line in input_file:
                        split = line.split('\t')
                        # print split
                        if len(split) == 3:
                            pos_x = int(split[0]) / resolution
                            pos_y = int(split[1]) / resolution

                            if pos_x > max_pos:
                                max_pos = pos_x
                            value = float(split[2])

                            if value > max_value:
                                max_value = value

                            cur.execute('INSERT INTO CacheDB VALUES (?,?,?)', (pos_x, pos_y, value,))

                        if i % 10000 == 0:
                            conn.commit()
                            print 'processed line: ', i

                        i += 1

                conn.commit()
                print 'creating index...'
                cur.execute('DROP INDEX IF EXISTS abc')
                cur.execute('CREATE INDEX abc ON CacheDB (PosX, PosY)')
                conn.commit()
    else:
        print 'index already exists. use -f to recreate it.'


    with open(config_file_name, 'wb') as json_file:
        json.dump({'resolution': resolution}, json_file, indent=4)

    print 'done.'


def main():
    parser = OptionParser(usage='usage: %prog [options] <input_file> <resolution> <output_project_dir>')
    # parser.add_option("-r", default=1000000, dest='resolution', help="resolution [%default]") # becomes an arg !
    parser.add_option("-f", default=False, action='store_true', dest='recache',
                      help="force rebuilting cache [%default]")

    (options, args) = parser.parse_args()
    print('config: ', options)
    if len(args) != 3:
        parser.print_help()
    else:
        run(args, options)


if __name__ == '__main__':
    main()
