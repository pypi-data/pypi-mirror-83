# PySizer

![](https://travis-ci.com/kumaraditya303/PySizer.svg?token=Tp128txvcHsePdipY3xq&branch=master)

![](https://img.shields.io/codecov/c/github/kumaraditya303/PySizer?style=flat-square)

# Introduction

### PySizer is a simple python command line program to resize images efficiently using Threads. This program uses click as a command line argument parser. It can also be used to pyinstaller to create a executable.

# Quick Start

- Install the project with pip

```bash
pip install git+https://github.com/kumaraditya303/PySizer.git
```

- Project will now be available as a command line utility

- Get Help

```text
$ pysizer.exe --help
Usage: pysizer [OPTIONS]

  Main PySizer function which with ThreadPoolExecutor creates threads for
  resizing pictures.

  Checks for correct file extension, creates threads for each picture with
  thread limitation as given by threads argument.

  Creates progress bar with the click for resizing progress.

Options:
  --source PATH      Pictures source  [default: .]
  --dest PATH        Destination for resized pictures  [default: resized]
  --height INTEGER   Image height  [default: 1280]
  --width INTEGER    Image weight  [default: 1920]
  --threads INTEGER  number of threads to use  [default: 40]
  --help             Show this message and exit.

```

# Project Made and Maintained By Kumar Aditya
