from Cython.Build import cythonize
import numpy as np
from distutils.core import setup
from distutils.extension import Extension

try:
    numpy_include = np.get_include()
except AttributeError:
    numpy_include = np.get_numpy_include()

ext_modules = [
    Extension(
        'bbox',
        sources=['bbox.c'],
        include_dirs = [numpy_include]
    ),
    Extension(
        'cython_nms',
        sources=['cython_nms.c'],
        include_dirs = [numpy_include]
    )
]
setup(
    ext_modules=ext_modules
)
