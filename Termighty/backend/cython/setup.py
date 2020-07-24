from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

modules = ['Color_Fast.pyx', 'Grid_Fast.pyx', 'Pixel_Fast.pyx',
           'Series_Fast.pyx', 'Style_Fast.pyx']
setup(
      ext_modules = cythonize("computed_types.pyx"),
      include_dirs = [numpy.get_include()]
     )
