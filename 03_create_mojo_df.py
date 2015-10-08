#!/usr/bin/python
# coding: utf-8
import json
from optparse import OptionParser
import cv2
import math
import numpy as np
import os
import re


def create_image_stack(args, options):
    dir_name = args[0]
    # print  options.name_config
    w_input_path = os.path.join(dir_name, options.name_config, 'mojo/images/tiles', 'w=' + str(0).zfill(8),
                                'z=00000000')
    config_file_name = os.path.join(dir_name, '_project', 'config.json')

    tif_name_splitter = re.compile('y=([0-9]+),x=([0-9]+)\.tif')

    if not os.path.isdir(w_input_path):
        print w_input_path + ' --> not a valid path'
        exit(1)

    # infer columns and rows from level 0 filenames
    all_file_names = [tif_name_splitter.search(f).groups() for f in os.listdir(w_input_path) if
                      os.path.isfile(os.path.join(w_input_path, f))]

    columns = max([int(xxx[0]) for xxx in all_file_names]) + 1
    rows = max([int(xxx[1]) for xxx in all_file_names]) + 1

    # infer tile size from first file in dir
    tile_size_file_name = os.path.join(w_input_path, 'y=' + str(0).zfill(8) + ',x=' + str(0).zfill(8) + '.tif')
    ts_img = cv2.imread(tile_size_file_name, cv2.IMREAD_UNCHANGED)

    size = (ts_img.shape[0], ts_img.shape[1])

    # THE OUTPUT SETTINGS
    tile_size = (512, 512)
    zoomlevels = int(math.ceil(math.log(max(columns, rows), 2)) + 1)

    #
    # CREATE MIPMAPS ONCE W=00000000 DICED IS THERE.
    #
    for w in range(1, zoomlevels):  # start with zoomlevel w=1

        w_width = columns * size[1] / 2 ** w
        w_height = rows * size[0] / 2 ** w
        w_columns = int(math.ceil(w_width / float(tile_size[1])))
        w_rows = int(math.ceil(w_height / float(tile_size[0])))

        w_output_path = os.path.join(dir_name, options.name_config, 'mojo/images/tiles', 'w=' + str(w).zfill(8),
                                     'z=00000000')

        if not os.path.exists(w_output_path):
            print 'Creating', w_output_path
            os.makedirs(w_output_path)

        for new_c in range(w_columns):
            for new_r in range(w_rows):

                prev_columns = range(new_c * 2, (new_c + 1) * 2)
                prev_rows = range(new_r * 2, (new_r + 1) * 2)

                output_file = 'y=' + str(new_r).zfill(8) + ',x=' + str(new_c).zfill(8) + '.tif'

                mojo_tile = np.zeros((tile_size[0] * 2, tile_size[1] * 2, 3), dtype=np.uint8)
                for i, prev_c in enumerate(prev_columns):
                    for j, prev_r in enumerate(prev_rows):
                        input_file = 'y=' + str(prev_r).zfill(8) + ',x=' + str(prev_c).zfill(8) + '.tif'
                        input_file_path = os.path.join(w_input_path, input_file)

                        if not os.path.exists(input_file_path):
                            # print 'ERROR', input_file_path
                            continue

                        prev_mojo_tile = cv2.imread(input_file_path, cv2.IMREAD_UNCHANGED)
                        mojo_tile[j * tile_size[0]:j * tile_size[0] + tile_size[0],
                        i * tile_size[1]:i * tile_size[1] + tile_size[1]] = prev_mojo_tile
                downsampled_mojo_tile = mojo_tile[::2, ::2]
                # downsampled_mojo_tile = cv2.pyrDown(mojo_tile,dstsize = (tile_size[0],tile_size[1]))
                output_file_path = os.path.join(w_output_path, output_file)
                cv2.imwrite(output_file_path, downsampled_mojo_tile)
                # print 'Written', output_file_path

        w_input_path = w_output_path
        print 'W =', w, 'done.'

    config = json.load(open(config_file_name, 'rb'))
    config['zoom_max'] = zoomlevels
    json.dump(config, open(config_file_name, 'wb'))


def main():
    parser = OptionParser(usage='usage: %prog [options] <project_directory>')
    parser.add_option("--name", default='', dest='name_config', help="name the current configuration [%default]")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
    else:
        print 'options', options
        create_image_stack(args, options)


if __name__ == '__main__':
    main()
