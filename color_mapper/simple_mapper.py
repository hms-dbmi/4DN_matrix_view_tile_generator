from matplotlib import cm
from matplotlib import colors

__author__ = 'Hendrik Strobelt'


class MatplotColorMapper:
    def __init__(self, color_space_name):
        self.color_space_name = color_space_name
        self.mapping_function = cm.get_cmap(color_space_name)

    def get_rgb_255(self, norm_value):
        # return [b * 255 for b in self.mapping_function(norm_value)[0:3]]
        return self.mapping_function(norm_value, alpha=None, bytes=True)[0:3]

    def get_rgb_255_array(self, norm_value):
        # return self.mapping_function(norm_value, alpha=None, bytes = True)
        # return [b * 255 for b in self.mapping_function(norm_value)[0:3]]
        return [a[0:3] for a in self.mapping_function(norm_value, alpha=None, bytes=True)]  # , bytes=True)]

    def get_bgr_255_array(self, norm_value):
        # return self.mapping_function(norm_value, alpha=None, bytes = True)
        # return [b * 255 for b in self.mapping_function(norm_value)[0:3]]
        return [a[2::-1] for a in self.mapping_function(norm_value, alpha=None, bytes=True)]  # , bytes=True)]
