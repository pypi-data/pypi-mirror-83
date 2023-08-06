# strup - string unpack

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/strup)](https://pypi.org/project/strup/)
[![CircleCI](https://img.shields.io/circleci/build/gh/jeblohe/strup?token=076c523c6a8f9a944a020eaca0d7074f05d77403)](https://circleci.com/gh/jeblohe/strup/tree/main)
[![Coveralls github](https://img.shields.io/coveralls/github/jeblohe/strup)](https://coveralls.io/github/jeblohe/strup)
[![Read the Docs](https://img.shields.io/readthedocs/strup)](https://strup.readthedocs.io/)
[![PyPI](https://img.shields.io/pypi/v/strup)](https://pypi.org/project/strup/)
[![Conda](https://img.shields.io/conda/v/jeblohe/strup)](https://anaconda.org/jeblohe/strup)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/jeblohe/strup/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://black.readthedocs.io/)

This Python package is for unpacking basic objects from a text string.
The standard data types **string**, **int**, **float** and **bool** are supported.

## Goals

A major goal with **strup** is to provide an intuitive interface.
If the standard [string methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
are too low level and the [re-module](https://docs.python.org/3/library/re.html)
adds too much complexity to your task, then **strup** might be your compromise.

Backward compatibility of this API is strongly emphasized.

## Usage

We apply the utility function **unpack(fmt, text)** for extracting
strings, ints, floats and bools from a text string **text**.
Each character in the string **fmt** defines the data type for the corresponding object.
 
```python
>>> from strup import unpack

>>> i, x, s, ok = unpack("ifs?", "5 2.3   ole  True")
>>> i, x, s, ok
(5, 2.3, 'ole', True)
```

Similar syntax is applied in the standard [struct](https://docs.python.org/3/library/struct.html) 
module for handling of binary data. However,
dots in the **fmt** string indicates that the corresponding item in **text** should be ignored.

```python
>>> unpack("f..s", " 2.3 ,ole,55,   dole", sep=',')      # sep as defined in string.split()
(2.3, '   dole')
```
Strings confined by quotes are supported

```python
>>> unpack("isf", "100 'Donald Duck' 125.6", quote="'")
(100, 'Donald Duck', 125.6)
```

Zero-sized string might be interpreted as **None** objects.

```python
>>> unpack("fissi", "2.3,,, ,12", sep=',', none=True)
(2.3, None, None, ' ', 12)
```


   
In loops you may benefit from splitting the grammar and the actual decoding using the class **Unpack**:

```python
>>> from strup import Unpack

>>> mydecode = Unpack('.s..f', quote='"')     # Preprocess the pattern
>>> for line in ['5.3 "Donald Duck" 2 yes 5.4',
                 '-2.2 "Uncle Sam" 4  no 1.5',
                 '3.3  "Clint Eastwood" 7 yes 6.5']:
...      mydecode(line)
("Donald Duck", 5.4)
("Uncle Sam", 1.5)
("Clint Eastwood", 6.5)
```

## Documentation

Complete [documentation](https://strup.readthedocs.io/) and more examples are hosted 
on [ReadTheDocs](https://readthedocs.org/).

## Source code

The source code for this package is located on [GitHub](https://github.com/jeblohe/strup).

## Installation

To install **strup** from PyPI:

```bash
pip install strup        # For end users
pip install -e .[dev]    # For package development (from the root of your strup Git repo)
```

or Anaconda:

```bash
conda install -c jeblohe strup
```

**strup** is continuously tested on Python 2.7, 3.4 and above.

## License

This software is licensed open-source under the MIT License.
