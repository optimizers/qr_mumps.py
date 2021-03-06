#!/usr/bin/env python

# The file setup.py is automatically generated
# Generate it with
# python generate_code -s

from distutils.core import setup
from setuptools import find_packages
from distutils.extension import Extension

import numpy as np

import ConfigParser
import os
import copy

from codecs import open
from os import path

# HELPERS
#--------
def prepare_Cython_extensions_as_C_extensions(extensions):
    """
    Modify the list of sources to transform `Cython` extensions into `C` extensions.
    Args:
        extensions: A list of (`Cython`) `distutils` extensions.
    Warning:
        The extensions are changed in place. This function is not compatible with `C++` code.
    Note:
        Only `Cython` source files are modified into their `C` equivalent source files. Other file types are unchanged.
    """
    for extension in extensions:
        c_sources = list()
        for source_path in extension.sources:
            path, source = os.path.split(source_path)
            filename, ext = os.path.splitext(source)

            if ext == '.pyx':
                c_sources.append(os.path.join(path, filename + '.c'))
            elif ext in ['.pxd', '.pxi']:
                pass
            else:
                # copy source as is
                c_sources.append(source_path)

        # modify extension in place
        extension.sources = c_sources

qr_mumps_config = ConfigParser.SafeConfigParser()
qr_mumps_config.read('site.cfg')

version = {}
with open("qr_mumps/version.py") as fp:
      exec(fp.read(), version)
# later on we use: version['version']

numpy_include = np.get_include()

# Use Cython?
use_cython = qr_mumps_config.getboolean('CODE_GENERATION', 'use_cython')
if use_cython:
    try:
        from Cython.Distutils import build_ext
        from Cython.Build import cythonize
    except ImportError:
        raise ImportError("Check '%s': Cython is not properly installed." % mumps_config_file)

# DEFAULT
default_include_dir = qr_mumps_config.get('DEFAULT', 'include_dirs').split(os.pathsep)
default_library_dir = qr_mumps_config.get('DEFAULT', 'library_dirs').split(os.pathsep)

# Debug mode
use_debug_symbols = qr_mumps_config.getboolean('CODE_GENERATION', 'use_debug_symbols')

# find user defined directories
qr_mumps_include_dirs = qr_mumps_config.get('QR_MUMPS', 'include_dirs').split(os.pathsep)
if qr_mumps_include_dirs == '':
    qr_mumps_include_dirs = default_include_dir
qr_mumps_library_dirs = qr_mumps_config.get('QR_MUMPS', 'library_dirs').split(os.pathsep)
if qr_mumps_library_dirs == '':
    qr_mumps_library_dirs = default_library_dir
           
# OPTIONAL
build_cysparse_ext = False           
if qr_mumps_config.has_section('CYSPARSE'):
    build_cysparse_ext = True
    cysparse_rootdir = qr_mumps_config.get('CYSPARSE', 'cysparse_rootdir').split(os.pathsep)
    if cysparse_rootdir == '':
        raise ValueError("You must specify where CySparse source code is" +
                         "located. Use `cysparse_rootdir` to specify its path.")


########################################################################################################################
# EXTENSIONS
########################################################################################################################
include_dirs = [numpy_include, '.']

ext_params = {}
ext_params['include_dirs'] = include_dirs
if not use_debug_symbols:
    ext_params['extra_compile_args'] = ["-O2", '-std=c99', '-Wno-unused-function']
    ext_params['extra_link_args'] = []
else:
    ext_params['extra_compile_args'] = ["-g", '-std=c99', '-Wno-unused-function']
    ext_params['extra_link_args'] = ["-g"]

context_ext_params = copy.deepcopy(ext_params)
qr_mumps_ext = []
{% for index_type in index_list %}
  {% for element_type in type_list %}
base_ext_params_@index_type@_@element_type@ = copy.deepcopy(ext_params)
base_ext_params_@index_type@_@element_type@['include_dirs'].extend(qr_mumps_include_dirs)
base_ext_params_@index_type@_@element_type@['library_dirs'] = qr_mumps_library_dirs
base_ext_params_@index_type@_@element_type@['libraries'] = [] # 'scalapack', 'pord']
base_ext_params_@index_type@_@element_type@['libraries'].append('@element_type|generic_to_qr_mumps_type@qrm')
base_ext_params_@index_type@_@element_type@['libraries'].append('qrm_common')
qr_mumps_ext.append(Extension(name="qr_mumps.src.qr_mumps_@index_type@_@element_type@",
                sources=['qr_mumps/src/qr_mumps_@index_type@_@element_type@.pxd',
                'qr_mumps/src/qr_mumps_@index_type@_@element_type@.pyx'],
                **base_ext_params_@index_type@_@element_type@))

numpy_ext_params_@index_type@_@element_type@ = copy.deepcopy(ext_params)
numpy_ext_params_@index_type@_@element_type@['include_dirs'].extend(qr_mumps_include_dirs)
qr_mumps_ext.append(Extension(name="qr_mumps.src.numpy_qr_mumps_@index_type@_@element_type@",
                 sources=['qr_mumps/src/numpy_qr_mumps_@index_type@_@element_type@.pxd',
                 'qr_mumps/src/numpy_qr_mumps_@index_type@_@element_type@.pyx'],
                 **numpy_ext_params_@index_type@_@element_type@))

  {% endfor %}
{% endfor %}

if build_cysparse_ext:
{% for index_type in index_list %}
  {% for element_type in type_list %}
    cysparse_ext_params_@index_type@_@element_type@ = copy.deepcopy(ext_params)
    cysparse_ext_params_@index_type@_@element_type@['include_dirs'].extend(cysparse_rootdir)
    cysparse_ext_params_@index_type@_@element_type@['include_dirs'].extend(qr_mumps_include_dirs)
    qr_mumps_ext.append(Extension(name="qr_mumps.src.cysparse_qr_mumps_@index_type@_@element_type@",
                 sources=['qr_mumps/src/cysparse_qr_mumps_@index_type@_@element_type@.pxd',
                 'qr_mumps/src/cysparse_qr_mumps_@index_type@_@element_type@.pyx'],
                 **cysparse_ext_params_@index_type@_@element_type@))

  {% endfor %}
{% endfor %}


packages_list = ['qr_mumps', 'qr_mumps.src']


# PACKAGE PREPARATION FOR EXCLUSIVE C EXTENSIONS
########################################################################################################################
# We only use the C files **without** Cython. In fact, Cython doesn't need to be installed.
if not use_cython:
    prepare_Cython_extensions_as_C_extensions(qr_mumps_ext)

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Developers
License :: OSI Approved
Programming Language :: Python
Programming Language :: Cython
Topic :: Software Development
Topic :: Scientific/Engineering
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS :: MacOS X
Natural Language :: English
"""

here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup_args = {
      'name' : 'qr_mumps.py',
      'version' : version['version'],
      'description' : 'A Cython/Python interface to the qr_mumps solver.',
      'long_description' : long_description,
      #Author details
{% raw %}
      'author' : 'Sylvain Arreckx, Dominique Orban and Nikolaj van Omme',
{% endraw %}
      'maintainer' : "Sylvain Arreckx",
{% raw %}
      'maintainer_email' : "sylvain.arreckx@gmail.com",
{% endraw %}
      'url' : "https://github.com/PythonOptimizers/qr_mumps.py",
      'download_url' : "https://github.com/PythonOptimizers/qr_mumps.py.git",
      'license' : 'LGPL',
      'classifiers' : filter(None, CLASSIFIERS.split('\n')),
      'install_requires' : ['numpy'],
      'ext_modules' : qr_mumps_ext,
      'package_dir' : {"qr_mumps": "qr_mumps"},
      'packages' : packages_list,
      'tests_requires' : ['pytest'],
      'setup_requires' : ['pytest-runner'],
      'zip_safe' : False}

if use_cython:
    setup_args['cmdclass'] = {'build_ext': build_ext}

setup(**setup_args)
