#!/usr/bin/env python
import os
import pathlib
import re
import subprocess
import sys

from setuptools import Command, find_packages, setup
from setuptools.extension import Extension


__author__ = "Peter Maxwell"
__copyright__ = "Copyright 2007-2020, The Cogent Project"
__contributors__ = [
    "Peter Maxwell",
    "Gavin Huttley",
    "Matthew Wakefield",
    "Greg Caporaso",
    "Daniel McDonald",
]
__license__ = "BSD-3"
__version__ = "2020.2.7a"
__maintainer__ = "Peter Maxwell"
__email__ = "pm67nz@gmail.com"
__status__ = "Production"

# Check Python version, no point installing if unsupported version inplace
min_version = (3, 6)
if sys.version_info < min_version:
    py_version = ".".join([str(n) for n in sys.version_info])
    msg = (
        f"Python-{'.'.join(min_version)} or greater is required, "
        f"Python-{py_version} used."
    )
    raise RuntimeError(msg)


# On windows with no commandline probably means we want to build an installer.
if sys.platform == "win32" and len(sys.argv) < 2:
    sys.argv[1:] = ["bdist_wininst"]


# A new command for predist, ie: pyrexc but no compile.
class NullCommand(Command):
    description = "Generate .c files from .pyx files"
    # List of option tuples: long name, short name (or None), and help string.
    user_options = []  # [('', '', ""),]

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        pass


class BuildDocumentation(NullCommand):
    description = "Generate HTML documentation files"

    def run(self):
        # Restructured Text -> HTML
        try:
            import sphinx
        except ImportError:
            print("Failed to build html due to ImportErrors for sphinx")
            return
        cwd = os.getcwd()
        os.chdir("doc")
        subprocess.call(["make", "html"])
        os.chdir(cwd)
        print("Built index.html")


short_description = "COmparative GENomics Toolkit 3"

readme_path = pathlib.Path(__file__).parent / "README.md"

long_description = readme_path.read_text()

PACKAGE_DIR = "src"

PROJECT_URLS = {
    "Documentation": "https://www.cogent3.org/",
    "Bug Tracker": "https://github.com/cogent3/cogent3/issues",
    "Source Code": "https://github.com/cogent3/cogent3",
}

setup(
    name="cogent3",
    version=__version__,
    url="https://github.com/cogent3/cogent3",
    author="Gavin Huttley",
    author_email="gavin.huttley@anu.edu.au",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=["any"],
    license=["BSD"],
    keywords=[
        "biology",
        "genomics",
        "statistics",
        "phylogeny",
        "evolution",
        "bioinformatics",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(where="src"),
    package_dir={"": PACKAGE_DIR},
    install_requires=["numba>0.48.0", "numpy", "scitrack", "tqdm", "tinydb"],
    extras_require={
        "dev": [
            "black",
            "click",
            "ipykernel",
            "ipywidgets",
            "isort",
            "jupyter_client",
            "jupyterlab",
            "jupytext",
            "nbconvert",
            "nbformat",
            "nbsphinx",
            "numpydoc",
            "pandas",
            "plotly",
            "psutil",
            "pytest",
            "pytest-azurepipelines",
            "pytest-cov",
            "pytest>=4.3.0",
            "sphinx",
            "sphinx-autobuild",
            "sphinxcontrib-bibtex",
            "tox",
        ],
        "extra": ["pandas", "plotly", "psutil"],
    },
    project_urls=PROJECT_URLS,
)
