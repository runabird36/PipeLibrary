from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
ext_modules = [
    Extension("SN_view",  ["source/SN_view.pyx"]),
]

setup(
    name = 'SearchNode',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)