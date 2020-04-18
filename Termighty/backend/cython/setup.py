from setuptools import setup
from Cython.Build import cythonize
from pathlib import Path
import numpy

build_path = Path.cwd() / 'Termighty' / 'backend' / 'cython'

modules = ['Color_Fast.pyx', 'Style_Fast.pyx', 'Pixel_Fast.pyx']#,
           # 'Grid_Fast.pyx']#, 'Series_Fast.pyx', ]

for i,j in enumerate(modules):
    modules[i] = str(build_path / j)

cds = {'language_level' : "3"}
params = {
          'ext_modules' : cythonize(modules, compiler_directives = cds),
          'include_dirs' : [numpy.get_include()]
         }

setup(**params)
