import math
import matplotlib.cm as mp_cm
import numpy as np
import cv2

__author__ = 'Hendrik Strobelt'


class ColorImageRenderer:
    def __init__(self, max_value, tile_size):
        self.max_value = max_value
        self.log_norm_max = math.log(max_value + 1)
        self.tile_size = tile_size
        self.colormap = mp_cm.get_cmap('Spectral')  # hot
        pass

    def norm(self, x, max_v):
        return math.log(x + 1) / max_v

    def create_img(self, cur, i, j, offset_x, offset_y, output_file):
        img = np.zeros((512, 512, 3), np.uint8)
        if i <= j:
            cur.execute('SELECT * FROM CacheDB WHERE PosX>=? AND PosX<? '
                        'AND PosY>=? AND PosY<?'
                        , (i * self.tile_size, (i + 1) * self.tile_size, j * self.tile_size, (j + 1) * self.tile_size))
            for row in cur.fetchall():
                a = self.norm(row[2], self.log_norm_max)
                img[int(row[0]) - offset_x, int(row[1]) - offset_y] = map(lambda b: b * 255, self.colormap(a)[0:3])

            cv2.imwrite(output_file, img)
            print i, j  # , ' <<<<< ', len(cur.fetchall())

        else:
            cv2.imwrite(output_file, img)

            print i, j  # , ' >>>> ', len(cur.fetchall())
