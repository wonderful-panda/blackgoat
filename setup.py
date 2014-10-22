# coding: utf-8
from distutils.core import setup
import py2exe

from py2exe.build_exe import py2exe as build_exe
import os
from glob import glob

package_data = {'blackgoat': ['templates/*.html']}

class ResourceCollector(build_exe):
    def copy_extensions(self, extensions):
        build_exe.copy_extensions(self, extensions)
        for pattern in [os.path.join(pkg, p)
                        for pkg in package_data for p in package_data[pkg]]:
            relpath = os.path.dirname(pattern)
            dest = os.path.join(self.collect_dir, relpath)
            if not os.path.exists(dest):
                self.mkpath(dest)
            for f in glob(pattern):
                name = os.path.basename(f)
                self.copy_file(f, os.path.join(dest, name))
                self.compiled_files.append(os.path.join(relpath, name))

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
    cmdclass = {'py2exe': ResourceCollector},
    packages = ['blackgoat'],
    package_data = package_data,
    requires = ['jinja2', 'sqlalchemy', 'flask', 'flask_script', 'flask_sqlalchemy'],
    console = ['blackgoat.py'],
    options = {'py2exe' : py2exe_option},
)
