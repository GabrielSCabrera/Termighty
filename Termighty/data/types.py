import numpy as np

str_types = (str)

arr_types = (list, tuple, np.ndarray)

uint_types = (np.uint8, np.uint16, np.uint32, np.uint64)

int_types = (int, np.int8, np.int16, np.int32, np.int64) + uint_types

float_types = (float, np.float32, np.float64)

real_types = int_types + float_types
