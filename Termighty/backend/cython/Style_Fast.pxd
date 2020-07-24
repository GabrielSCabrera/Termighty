import numpy as np
cimport numpy as np

cdef class Style_Fast(object):

  '''INSTANCE ATTRIBUTES'''
  cdef public str sequence
  cdef public list codes
  cdef public list styles_list
  cdef public np.uint8_t[:] arr

  '''ACCESSORS'''
  cpdef list styles(self)

  '''GETTERS'''
  cpdef np.uint8_t[:] as_arr(self)

  '''MANAGERS'''
  cpdef void update(self)

  '''COMPARATORS'''

  cpdef bint eq(self, style)
  cpdef bint ne(self, style)
