# PyoFormats
Simple wrapper for python-formats
---
## Example
```python
from pyoformats import read

# start JVM
read.JVM().start()

# displays names and shapes of all available series in file
read.file_info("test.msr")

# get series count of file
n_series = read.series_count("test.msr")

# returns 5d numpy array of image in series
my_image = read.image_5d("test.msr", series=1)

# read only certain z-slices. (Note, also channels and frames can be selected)
my_image = read.image_5d("test.msr", series=1, zslices=[2, 3, 5, 8, 13])

# get physical pixel sizes
xyz_sizes = read.pixel_sizes_xyz("test.msr", series=0)

# get physical pixel units
xyz_sizes = read.pixel_sizes_xyz_units("test.msr", series=0)

# iterate over all series and extract name and pixel data
for s, data in read.image_5d_iterator("test.msr"):
    print(s, data.shape)


# at end of script
read.JVM().shutdown()
```

## Installation

#### Detailed How-To for installing dependencies (Windows/ MacOS)

Before you install the pyformats Python package, check out detailed instructions for [installing dependencies](Installation.md).

#### pyoformats directly from gitlab
`pip install git+https://git.ist.ac.at/csommer/pyoformats.git`

#### or local

1. `git clone https://git.ist.ac.at/csommer/pyoformats.git`
2. `cd pyoformats`
3.  `pip install -e .`

## Dependencies
* numpy
* javabridge
* python-bioformats

