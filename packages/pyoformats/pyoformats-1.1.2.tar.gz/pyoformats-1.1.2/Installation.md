# Installation Instructions for Windows and Mac

In order to get the pyoformats working, we need to install a bunch of software. This is mostly due to the python-bioformats, javabridge and python-javabridge packages, which in turn are needed to use the OME bioformats framework (originally written for FIJI).  

These instructions are intended for people with little prior programming experience. If you have prior experience, you probably have a bunch or all of these tools already installed.  

Tested October 2020 on several PCs and Macs in the Danzl group  
Windows 10  
Mac OS Catalina 10.15.6  

## Install all required software and tools

### Install a Java Development Kit (JDK)

We tested with the JDK LTS 11 (11.0.8)  
Download: https://www.oracle.com/java/technologies/javase-jdk11-downloads.html, select your operating system.  
If you’re on Mac, the JDK has to be added to your path manually. This step may be a bit tricky, I followed this post: https://stackoverflow.com/questions/12089697/how-to-set-java-jdk-environment-variable-for-mac-os-x-10-8-mountain-lion. If you’ve never used vim or are uncomfortable using the terminal, let me know and I’ll set it up for you.  

### Install Git

Needed to install packages directly from git (if they're not available in the python repositories).  
The installer has a lot of options, we just picked the ones that sounded least experimental / most default.  
Download for Mac: https://sourceforge.net/projects/git-osx-installer/  
Download for Windows: https://git-scm.com/download/win (Pick the 64 bit installer)  

### On Windows: Install visual studio build tools

Needed to install javabridge package.  
Download: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16  
Alternatively: https://visualstudio.microsoft.com/downloads/, navigate to "Tools for visual studio", select "build tools for visual studio"  
On the first page of the installer, select the first tile (Visual C++ build tools). Leave all other options default.  

### On Mac: Install xcode command line tools

Needed to install javabridge package, equivalent to the visual studio build tools on windows (?)  
Download: https://developer.apple.com/download/more/?=command%20line%20tools  
We tested with Command Line Tools for XCode 12.  
You need to setup a developer account with apple to download these.  

### Install Anaconda

This is the python distribution we're using. Leave all options of the installer default.  
Download: https://www.anaconda.com/products/individual  

## Setup the actual python environment 

Now, we have to install the python packages that we need for everything to work. The easiest way to do that is using command line tools.  
- on Windows, open AnacondaPrompt as administrator (do not use the the windows command line, installation of javabridge fails, and installation from wheel just succeeded for an old version with a bug that prevents opening stacks correctly)  
- on Mac, open the Terminal  

Then type / copy paste the following line-by-line (I’m putting explanations in brackets)  

### Create and activate the python environment

_conda create -n pyoformats python=3.8.5_  
Conda is the python package manager that comes with anaconda. It’s essentially making sure that, when you install new packages, they are compatible with all the other things you have already installed and that the new package finds all the dependencies it needs.  
Here, we’re telling conda to create a new environment named “pyoformats”. An environment is a own little python universe. You can have as many different ones as you want. They’re a convenient way of making sure that installing packages into one environment does not destroy your 10 years old workflow requiring deprecated packages in the other.  

Confirm all dialogues by typing y<enter>  

_conda activate pyoformats_  
We swap to the newly created environment. You should now see that (base) in the terminal has changed to pyoformats.  

### Install some required packages manually

_conda install -c conda-forge jupyterlab_  
(Install jupyterlab from conda-forge using conda. It’s the interactive python “editor” we’re going to use.  

_pip install numpy_  
There's an unfortunate bug in python 3.8 where installations requiring numpy fail. We therefore install numpy manually.  
Pip is another package manager … long story … some packages are simply not available using conda. We need pip anyway in the next step, and also  use it here to install numpy.  

### Install the actually required package

_pip install tifffile pyqt5 napari git+https://git.ist.ac.at/csommer/pyoformats.git_  
Use pip to install the packages tifffile, pyqt5, napari and pyoformats. tifffile, pyqt5, napari are not needed for pyoformats, but very handy for image analysis in python.  

On Mac, installation of the javabridge required for pyoformats sometimes fails. If that's the case, install javabridge directly from source: (Solution found here: https://github.com/LeeKamentsky/python-javabridge/issues/169)  
_pip install git+https://github.com/LeeKamentsky/python-javabridge.git#egg=javabridge_  

then retry  
_pip install tifffile pyqt5 napari git+https://git.ist.ac.at/csommer/pyoformats.git_  

You should be all set!  