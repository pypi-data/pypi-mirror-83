from setuptools import setup, find_packages
from codecs import open
import os


# Get the long description from the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    long_description = f.read()

# Get the version
for line in open(os.path.join(here, "strup", "__init__.py")):
    if line.startswith("__version__"):
        version = line.split("=")[1].strip()[1:-1]


# List packages we depend on (end users)
dependencies = []

# Packages for development of strup (assumed on Python 3.x)
dependencies_dev = ["pytest>=5.1", "pytest-cov", "coverage", "black", "coveralls"]
# Packages for testing strup without syntax and coverage checks (for CI checks on old images)
dependencies_test = ["pytest>=4.6"]

setup(
    name="strup",
    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=version,
    description=(
        "A package for unpacking int, float, string and bool objects from a text string."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    # The project's main homepage.
    url="https://github.com/jeblohe/strup",
    # Author details
    author="Jens B. Helmers",
    author_email="jens.bloch.helmers@gmail.com",
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 5 - Production/Stable",
        # Indicate who your project is intended for
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Text Processing",
        # Pick your license as you wish (should match "license" above)
        "License :: OSI Approved :: MIT License",
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    # Supported Python versions (pip will refuse to install on other versions)
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4",
    # What does your project relate to?
    keywords="text processing",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed.
    install_requires=dependencies,
    # List additional groups of dependencies here (e.g. development and test
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install strup[dev]       # or:  pip install -e .[dev]
    #   $ pip install strup[test]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    extras_require={
        "dev": dependencies_dev,
        "test": dependencies_test,
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={},
    zip_safe=True,
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={"console_scripts": []},
    # List additional URLs that are relevant to your project as a dict.
    project_urls={
        "Documentation": "https://strup.readthedocs.io/",
        "Bug Tracker": "https://github.com/jeblohe/strup/issues",
        "Source Code": "https://github.com/jeblohe/strup/",
    },
)
