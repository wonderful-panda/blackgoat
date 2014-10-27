# coding: utf-8
from distutils.core import setup
__import__('py2exe') # to avoid pep8 warning 'Imported but unused'

import os
from glob import glob
from itertools import groupby

def gather_data_files(dest, root, pattern):
    def getdest(relpath):
        relpath = relpath[len(root) + 1:]
        if relpath:
            return os.path.join(dest, relpath)
        else:
            return dest

    files = sorted(glob(os.path.join(root, pattern)))
    return [(getdest(key), list(group))
            for (key, group) in groupby(files, os.path.dirname)]

data_files = \
        [('', ['config.yaml']), ('log', [])] + \
        gather_data_files('templates', 'blackgoat/templates', '*.html') + \
        gather_data_files('static', 'blackgoat/static', '*/**/*.*') 

py2exe_option = \
    dict(
            packages = ['jinja2', 'flask_script', 'flask_sqlalchemy'],
            excludes = ['tcl', 'Tkconstants', 'Tkinter'],
            compressed = 1,
            optimize = 2,
            bundle_files = 1,
        )

setup(
    name = 'blackgoat',
    #cmdclass = {'py2exe': ResourceCollector},
    packages = ['blackgoat'],
    data_files = data_files,
    requires = ['jinja2', 'sqlalchemy', 'flask', 'flask_script', 'flask_sqlalchemy'],
    console = ['blackgoat.py'],
    options = {'py2exe' : py2exe_option},
)
