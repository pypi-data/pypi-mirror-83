import pathlib
from setuptools import setup

# The directory containing this file
_this_dir = pathlib.Path(__file__).parent

# The text of the README file
long_description = (_this_dir / "README.md").read_text()

# Exec version file
exec((_this_dir / "pyoformats" / "version.py").read_text())

setup(
    name="pyoformats",
    packages=["pyoformats"],
    version=__version__,
    description="PyoFormats: Simple wrapper for python-bioformats",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.ist.ac.at/csommer/pyoformats",
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
    ],
    #    entry_points = {'console_scripts': []},
    author="Christoph Sommer, Wiebke Jahr",
    author_email="christoph.sommer23@gmail.com, wiebke.jahr@ist.ac.at",
    install_requires=["numpy", "javabridge", "python-bioformats",],
)

