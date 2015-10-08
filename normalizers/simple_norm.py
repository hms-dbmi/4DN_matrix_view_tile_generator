import math

__author__ = 'Hendrik Strobelt'


class StdNormalizer:
    def __init__(self, max_value):
        self.max_value = max_value

    def norm(self, value):
        return 1


class LogNormalizer(StdNormalizer):
    def __init__(self, max_value):
        self.max_log_value = math.log(max_value + 1)

    def norm(self, value):
        return math.log(value + 1) / self.max_log_value


class LinNormalizer(StdNormalizer):
    def norm(self, value):
        return value / self.max_value
