import matplotlib.cm as mp_cm
import numpy as np
import cv2
from normalizers.simple_norm import *

__author__ = 'Hendrik Strobelt'


class ColorImageRenderer:
    def __init__(self, max_value, tile_size, normalizer, color_mapper):
        self.max_value = float(max_value)
        self.tile_size = tile_size
        self.colormap = color_mapper
        self.normalizer = normalizer
        pass

    def norm(self, x, max_v):
        return math.log(x + 1) / max_v

    def create_img(self, cur, i, j, offset_x, offset_y, output_file):
        img = np.zeros((512, 512, 3), np.uint8)
        if i <= j:
            cur.execute('SELECT * FROM CacheDB WHERE PosX>=? AND PosX<? '
                        'AND PosY>=? AND PosY<?'
                        , (i * self.tile_size, (i + 1) * self.tile_size, j * self.tile_size, (j + 1) * self.tile_size))
            # for row in cur.fetchall():
            #     a = self.normalizer.norm(row[2])
            #     img[int(row[0]) - offset_x, int(row[1]) - offset_y] = self.colormap.get_rgb_255(a)
            all_pos = cur.fetchall()
            all_colors = self.colormap.get_bgr_255_array([self.normalizer.norm(row[2]) for row in all_pos])

            for index, row in enumerate(all_pos):
                img[int(row[0]) - offset_x, int(row[1]) - offset_y] = all_colors[index]

            cv2.imwrite(output_file, img)
            print i, j  # , ' <<<<< ', len(cur.fetchall())

        else:
            cv2.imwrite(output_file, img)

            print i, j  # , ' >>>> ', len(cur.fetchall())
