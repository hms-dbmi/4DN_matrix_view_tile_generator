#!/usr/bin/python
from optparse import OptionParser
import os
import sqlite3
from image_generators.color_tiff import ColorImageRenderer

__author__ = 'Hendrik Strobelt'


def run(args, options):
    project_dir = os.path.join(args[0], '_project')
    index_file_name = os.path.join(project_dir, 'index.sqlite')
    config_file_name = os.path.join(project_dir, 'config.json')
    tile_size = int(options.tile_size)
    if options.mojo_fs:
        output_dir_name = os.path.join(args[0], options.name_config, 'mojo/images/tiles', 'w=' + str(0).zfill(8),
                                       'z=00000000')
    else:
        output_dir_name = os.path.join(args[0], options.name_config, 'images')

    if not os.path.isdir(project_dir):
        print project_dir, ' could not be found.'
        exit(1)

    if not os.path.isfile(index_file_name):
        print index_file_name, ' - index file not found.'
        exit(1)


    if not os.path.exists(output_dir_name):
        os.makedirs(output_dir_name)

    conn = sqlite3.connect(index_file_name)
    with conn:
        cur = conn.cursor()

        # get max data
        cur.execute('SELECT max(PosX),max(PosY),max(Value) FROM CacheDB')
        max_x, max_y, max_v = cur.fetchone()
        max_all = max(max_x, max_y)

        no_tiles = int(max_all / tile_size) + 1

        image_renderer = ColorImageRenderer(max_v, tile_size)


        print(no_tiles, max_x, max_y, max_v)

        for i in range(0, no_tiles):
            for j in range(0, no_tiles):

                offset_x = i * tile_size
                offset_y = j * tile_size

                output_file = os.path.join(output_dir_name,
                                           'y=' + str(i).zfill(8) + ',x=' + str(j).zfill(8) + '.tif')
                print output_file
                image_renderer.create_img(cur, i, j, offset_x, offset_y, output_file)


def main():
    parser = OptionParser(usage='%prog [options] <project_directory>',
                          description=' !! The project_directory has to be created by a 01_* script !!')
    parser.add_option("-t", default=512, dest='tile_size', help="define  size of tiles [%default]")
    parser.add_option("-m", default=True, action='store_false', dest='mojo_fs', help="don't create a mojo fs")
    parser.add_option("--name", default='', dest='name_config', help="name the current configuration [%default]")

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
    else:
        print(options)
        run(args, options)


if __name__ == '__main__':
    main()
