# Text Analyzer

**TextAnalyzer** is a command line client, written in Python, capable of reading in and analyzing text from a variety of sources, including strings, local files, and webpages on the Internet.

## Getting Started

### Prerequisites

---

#### Python

This project is compatible with _both_ __Python 2.x__ and __Python 3.x__, so you need to first install one of these versions of the Python interpreter.

To install a Python interpreter for running this code, please visit the [Python Downloads](https://www.python.org/downloads/) page and click on either the button labeled **Download Python 2.7.x** or the one labeled **Download Python 3.6.x**.

![Downloads Page for Python Interpreter](https://www.ics.uci.edu/~pattis/common/handouts/pythoneclipsejava/images/python/pythondownloadpage.jpg)

To check if __Python 2.x__ is installed, open __Console__ (Linux), __Terminal__ (MacOS), or __Command Prompt__ (Windows) and type the following:

    python --version

If you see something like ``python 2.7.9``, then you're ready to go!

To check if __Python 3.x__ is installed, follow the same instructions as above, but type in the following at the prompt:

    python3 --version

If you see something like ``python 3.6.0``, then you're ready to continue with the rest of the installation.

#### Requests

In order to support text analysis on webpages, this project makes use of the the [Requests](http://docs.python-requests.org/en/master/) library.

To install the Requests library, type in the following in your console / command prompt:

    pip install requests

#### Matplotlib (Optional)

If you would like to use the included ``graph.py`` as a library, you need to install matplotlib as follows:

    pip install matplotlib

After completing the above steps, you should be ready to run the program, as specified below.

### Usage

---

#### print usage info

    python main.py -h

#### analyze strings directly

    python main.py -s 'Hello, World!' 'Strings are great'

#### analyze text from local files

    python main.py -f poem.txt speech.txt ../conversation.txt

#### analyze text on the Web

    python main.py -u http://www.example.com

## Built With

---

* Python - https://www.python.org
* Requests - http://docs.python-requests.org/en/master/
* Matplotlib - http://www.matplotlib.org

## Author

---

* **Syed Peer**

## Acknowledgments

---

* Thanks to [Kenneth Reitz](https://github.com/kennethreitz) for the [Requests](http://docs.python-requests.org/en/master/) library