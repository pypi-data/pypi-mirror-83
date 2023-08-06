# CASParser
[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub](https://img.shields.io/github/license/codereverser/casparser)](https://github.com/codereverser/casparser/blob/main/LICENSE)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/casparser)

Parse Consolidated Account Statement (CAS) PDF files generated from CAMS/KFINTECH


## Installation
```bash
pip install casparser
``` 

## Usage

```
import casparser
data = casparser.read_cas_pdf('/path/to/cas/pdf/file.pdf', 'password')
```

#### CLI

```bash
Usage: casparser [-o output_file.json] [-p password] [-s] CAS_PDF_FILE

Options:
  -o, --output FILE  Output file path (json)
  -s, --summary      Print Summary of transactions parsed.
  -p PASSWORD        CAS password
  --version          Show the version and exit.
  --help             Show this message and exit.
``` 

##### Demo

![demo](https://raw.githubusercontent.com/codereverser/casparser/main/assets/demo.jpg)