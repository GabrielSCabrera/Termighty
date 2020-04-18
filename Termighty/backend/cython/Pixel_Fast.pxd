import numpy as np
cimport numpy as np

cdef class Pixel_Fast(object):

  '''INSTANCE ATTRIBUTES'''
  cdef public object color_t_obj
  cdef public object color_b_obj
  cdef public object style_obj
  cdef public str char_str
  cdef public str out

  '''ACCESSORS'''
  cpdef object color_t(self)
  cpdef object color_b(self)
  cpdef object style(self)
  cpdef str char(self)

  '''GETTERS'''
  cpdef np.uint64_t[:] as_arr(self)

  '''SETTERS'''
  cpdef void set_color_t(self, object color)
  cpdef void set_color_b(self, object color)
  cpdef void set_style(self, object style)
  cpdef void set_char(self, str character)

  '''FORMATTERS'''
  cpdef str color_t_seq(self)
  cpdef str color_b_seq(self)
  cpdef str style_seq(self)
  cpdef str end_seq(self)

  '''MANAGERS'''
  cpdef void update(self)

  '''COMPARATORS'''
  cpdef bint eq(self, object pixel)
  cpdef bint ne(self, object pixel)
