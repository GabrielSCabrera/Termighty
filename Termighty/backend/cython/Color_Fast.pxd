import numpy as np
cimport numpy as np

cdef class Color_Fast(object):

  '''INSTANCE ATTRIBUTES'''
  cdef public str name_str
  cdef public np.uint8_t[:] RGB_arr

  '''SETTER METHODS'''
  cpdef void set_name(self, str name)
  cpdef void set_RGB(self, tuple RGB)
  cpdef void set_R(self, int R)
  cpdef void set_G(self, int G)
  cpdef void set_B(self, int B)

  '''GETTER METHODS'''
  cpdef str name(self)
  cpdef tuple RGB(self)
  cpdef int R(self)
  cpdef int G(self)
  cpdef int B(self)

  '''SAMPLER METHODS'''
  cpdef str sample(self)

  '''COMPARATORS'''
  cpdef bint eq(self, color)
  cpdef bint ne(self, color)
  cpdef bint lt(self, color)
  cpdef bint gt(self, color)
  cpdef bint le(self, color)
  cpdef bint ge(self, color)
