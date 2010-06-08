#!/usr/env/python
"""StringMap

"""
from __future__ import unicode_literals
import logging
import pprint
import random
from math import sqrt


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

    def set_all_columns_for_row(self, row, to=None):
        for _i in xrange(self.columns):
            self.matrix.setitem(row, _i, to)

    def set_all_rows_for_column(self, col, to=None):
        for _i in xrange(self.rows):
            self.matrix.setitem(_i, col, to)

    def __repr__(self):
        return pprint.pformat(self.matrix)


class StringMap(object):

    def __init__(self, string_list, dimensionality, metric_function):
        self.string_list = string_list
        self.dimensionality = dimensionality
        self.metric_function = metric_function
        # 2 x d pivot strings
        self.pivot_matrix = Matrix(2, dimensionality, initializer='')
        # N x d object coordinates
        self.coords = Matrix(len(string_list), dimensionality)
        # seed random
        random.seed()

    def mapify(self):
        for axis in xrange(0, self.dimensionality):
            pivot1, pivot2 = self.choose_pivot_strings(axis)
            # store them in the matrix
            self.pivot_matrix.setitem(0, axis, self.string_list[pivot1])
            self.pivot_matrix.setitem(1, axis, self.string_list[pivot2])
            dist = self.get_distance(pivot1, pivot2, axis)
            if dist == 0:
                # set all coordinates to the h-th dimension to 0
                self.coords.set_all_rows_for_column(axis, 0)
                break
            # compute coordinates of strings on this axis
            for i in xrange(len(self.string_list)):
                x = self.get_distance(i, pivot1, axis)
                y = self.get_distance(i, pivot2, axis)
                self.coords.setitem(i, axis, self.calculate_coord(x, y, dist))

    def calculate_coord(self, x, y, dist):
        return (pow(x, 2) + pow(dist, 2) - pow(y, 2)) / (2 * dist))

    def choose_pivot_strings(self, axis, m=5):
        """Chooses two pivot strings on the h-th dimension"""
        random_string = random.choice(self.string_list)

        return 0, 0

    def get_distance(self, coord_a, coord_b, axis):
        """Get distance of two strings (indexed by coord_a and coord_b)
        after they are projected on the first h - 1 axes

        """
        string_a = self.string_list[coord_a]
        string_b = self.string_list[coord_b]
        metric_distance = self.metric_function(string_a, string_b)
        for i in xrange(axis):
            w = self.coords[coord_a, i] - self.coords[coord_b, i]
            metric_distance = sqrt(abs(pow(metric_distance, 2) - pow(w, 2)))

        return metric_distance
