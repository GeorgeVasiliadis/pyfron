# pyfron
An OpenDR-based face recognition CLI app

## Why pyfron
This package provides an easy-to-use methodology for:

- Creating OpenDR face recognizers
- Manipulating several image databases with environments
- Reporting the overall performance of recognizers in beautiful markdowns

## Installation
1. Manually [install OpenDR](https://github.com/opendr-eu/opendr#installing-opendr-toolkit)
2. Run `pip install pyfron`
3. Optionally, you may download the [LFW](http://vis-www.cs.umass.edu/lfw/) image database and set up its structure (see below)

## Structures

The terms "image directory" and "image database" are used interchangeably. They both refer to a directory housing 
a single subdirectory called `"images"` which contains more subdirectories representing different people. Each one of those 
may contain an arbitrary number of `*.jpg` files.
 
#### Here's an overview of an image directory named `"my_db"`:
 ```
my_db/
|--- images/
|    |--- thats_a_person_dir/
|    |    |--- first.jpg
|    |    |--- ...
|    |    |--- last.jpg
|    |--- thats_another_person_dir/
|    |    |--- 1.jpg
|    |--- ...
|    |--- last_person/
```

## Quick Start

