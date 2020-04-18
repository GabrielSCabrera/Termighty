import numpy as np
cimport numpy as np

cdef class Grid_Fast(object):
  '''INSTANCE ATTRIBUTES'''
  cdef np.data
  cdef np.shape_arr
