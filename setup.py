#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from distutils.core import setup

PACKAGE = 'sanaviron'
APP_VERSION='0.1.0'

if __name__ == '__main__':
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    excludes = ['.', '..','.svn','src','images','examples']
    packages, datafiles = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir:
        os.chdir(root_dir)
    
    for dirpath, dirnames, filenames in os.walk(PACKAGE):
        for i, dirname in enumerate(dirnames):
            if dirname in excludes:
                del dirnames[i]
        if '__init__.py' in filenames:
            pkg = dirpath.replace(os.path.sep, '.')
            if os.path.altsep:
                pkg = pkg.replace(os.path.altsep, '.')
            packages.append(pkg)
        elif filenames:
            prefix = dirpath[len(PACKAGE) + 1:] # Strip package directory + path separator
            for f in filenames:
                datafiles.append(os.path.join(prefix, f))

setup(
    name=PACKAGE,
    version=APP_VERSION,
    scripts=['bin/sanaviron'],
    packages=packages,
    package_data = {PACKAGE: datafiles},
    data_files = [('/usr/share/applications',['bin/sanaviron.desktop']),
                  ('/usr/share/icons',['bin/sanaviron.png']),
                  (os.path.join('/usr/share/doc',PACKAGE),['COPYING']), # TODO: Include help files here
                 ],
    url='http://code.google.com/p/sanaviron/',
    license='Apache License 2.0',
    author='Juan Manuel Mouriz, Ivlev Denis',
    author_email='jmouriz@sanaviron.org, ivlevdenis.ru@gmail.com',
    description='The Sanaviron Project is an 2D drawing engine fully written in Python for represent composite vector graphics. This is essentially a GTK+ Cairo based canvas.',
    long_description=open('README').read(),
)
