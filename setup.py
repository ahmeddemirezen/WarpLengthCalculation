from distutils.core import setup
import py2exe
import sys
import os
import matplotlib
print(matplotlib.pyplot.get_backend())
matplotlib.use('wxagg')
print(matplotlib.pyplot.get_backend())
import MainWindow

sys.argv.append('py2exe')

setup(
    options={'py2exe': {'includes': ['matplotlib.numerix.random_array',"matplotlib.backends.backend_tkagg","packaging.specifiers","packaging.version","packaging.requirements","matplotlib"], 'excludes': [
        '_gtkagg', '_tkagg'], 'dll_excludes': ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll']}},
    windows=[{'script': "main.py"}],
    zipfile=None,
)
