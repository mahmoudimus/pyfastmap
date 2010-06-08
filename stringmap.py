#!/usr/env/python
"""StringMap

"""
from __future__ import unicode_literals
from itertools import count
import logging
import pprint


logger = logging.getLogger(__name__)


class Matrix(object):
    """A simple matrix implementation"""
    def __init__(self, rows, cols,  initializer=0):
        self.rows = rows
        self.columns = cols
        self.matrix = []

        for _i in xrange(rows):
            ea_row = []
            for _j in xrange(cols):
                ea_row.append(initializer)
            self.matrix.append(ea_row)

    def __iter__(self):
        for row in range(self.rows):
            for col in range(self.columns):
                yield (self.matrix, row, col)

    def setitem(self, row, col, v):
        self.matrix[row][col] = v

    def getitem(self, row, col):
        return self.matrix[row][col]

    def __repr__(self):
        return pprint.pformat(self.matrix)


class StringMap(FastMap):

    def __init__(self, string_list, dimensionality, metric_function):
        self.string_list = string_list
        self.dimensionality = dimensionality
        self.metric_function = metric_function
        # 2 x d pivot strings
        self.pivot_array = Matrix(2, dimensionality, initializer='')
        # N x d object coordinates
        self.coords = Matrix(len(string_list), dimensionality)

    def mapify(self):
        for axis in count(1):
            if axis > self.dimensionality:
                break
            px, py = self._pickPivot()
