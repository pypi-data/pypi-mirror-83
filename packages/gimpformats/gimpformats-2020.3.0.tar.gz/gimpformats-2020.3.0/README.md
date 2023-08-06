[![GitHub top language](https://img.shields.io/github/languages/top/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](../../)
[![Codacy grade](https://img.shields.io/codacy/grade/fc44ef973e9048f3840deaa85a1975d9.svg?style=for-the-badge)](https://www.codacy.com/gh/FHPythonUtils/GimpFormats)
[![Repository size](https://img.shields.io/github/repo-size/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](../../)
[![Issues](https://img.shields.io/github/issues/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](../../issues)
[![License](https://img.shields.io/github/license/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](/LICENSE.md)
[![Commit activity](https://img.shields.io/github/commit-activity/m/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](../../commits/master)
[![Last commit](https://img.shields.io/github/last-commit/FHPythonUtils/GimpFormats.svg?style=for-the-badge)](../../commits/master)
[![PyPI Downloads](https://img.shields.io/pypi/dm/gimpformats.svg?style=for-the-badge)](https://pypi.org/project/gimpformats/)
[![PyPI Version](https://img.shields.io/pypi/v/gimpformats.svg?style=for-the-badge)](https://pypi.org/project/gimpformats/)

<!-- omit in TOC -->
# GimpFormats

<img src="readme-assets/icons/name.png" alt="Project Icon" width="750">

Forked from https://github.com/TheHeadlessSourceMan/gimpFormats

A pure python implementation of the GIMP XCF image format. Use this to interact
with GIMP image formats

Issues and contributions very much wanted/ needed :smile:

Previously under `gimpformats_unofficial` now under `gimpformats`

- [Getting started](#getting-started)
- [Next tasks (see below)](#next-tasks-see-below)
- [Currently supports](#currently-supports)
- [In progress but results in crashes and tests failing](#in-progress-but-results-in-crashes-and-tests-failing)
- [Not implemented](#not-implemented)
- [Install With PIP](#install-with-pip)
- [Language information](#language-information)
	- [Built for](#built-for)
- [Install Python on Windows](#install-python-on-windows)
	- [Chocolatey](#chocolatey)
	- [Download](#download)
- [Install Python on Linux](#install-python-on-linux)
	- [Apt](#apt)
- [How to run](#how-to-run)
	- [With VSCode](#with-vscode)
	- [From the Terminal](#from-the-terminal)
- [How to update, build and publish](#how-to-update-build-and-publish)
- [Download](#download-1)
	- [Clone](#clone)
		- [Using The Command Line](#using-the-command-line)
		- [Using GitHub Desktop](#using-github-desktop)
	- [Download Zip File](#download-zip-file)
- [Community Files](#community-files)
	- [Licence](#licence)
	- [Changelog](#changelog)
	- [Code of Conduct](#code-of-conduct)
	- [Contributing](#contributing)
	- [Security](#security)

## Getting started

Read an image
```python
from gimpformats.gimpXcfDocument import GimpDocument
project = GimpDocument("image.xcf")
```

Iterate the image and report the contents of each group followed by the first
level children of the image
```python
"""List data on groups followed by the direct children of a gimp xcf document
"""
layers = project.layers
index = 0
print("## Group info...")
while index < len(layers):
	layerOrGroup = layers[index]
	if layerOrGroup.isGroup:
		index += 1
		while layers[index].itemPath is not None:
			print("Group \"" + layerOrGroup.name + "\" contains Layer \"" + layers[index].name + "\"")
			layers.pop(index)
	else:
		index += 1

print("## Document direct children...")
for layerOrGroup in layers:
	print("\"" + layerOrGroup.name + "\" is a " + ("Group" if layerOrGroup.isGroup else "Layer"))

```

Example output:

```none
## Group info...
Group "Layer Group" contains Layer "Layer"
Group "Layer Group" contains Layer "Layer2"
## Document direct children...
"bg #1" is a Layer
"bg" is a Layer
"bg #2" is a Layer
"Transformation" is a Layer
"Layer Group" is a Group
"Background" is a Layer
```

## Next tasks (see below)
- Saving

## Currently supports
- Loading xcf files (up to current GIMP version 2.10)
- Getting image hierarchy and info
- Getting image for each layer (PIL image)
- .gbr brushes
- .vbr brushes
- .gpl palette files
- .pat pattern files
- .gtp tool presets
- Generate a flattened image
- Add new layers

## In progress but results in crashes and tests failing
- Saving
- .ggr gradients - reads/saves fine, but I need to come up with a way to get the
actual colours
- .gih brush sets - BUG: seems to have more image data per brush than what's
expected
- .gpb brush - should work, but I need some test files

## Not implemented
- Exported paths in .svg format. - Reading should be easy enough, but I need to
ensure I don't get a full-blown svg in the mix
- Standard "parasites"

## Install With PIP

```python
pip install gimpformats
```

Head to https://pypi.org/project/gimpformats/ for more info

## Language information
### Built for
This program has been written for Python 3 and has been tested with
Python version 3.8.0 <https://www.python.org/downloads/release/python-380/>.

## Install Python on Windows
### Chocolatey
```powershell
choco install python
```
### Download
To install Python, go to <https://www.python.org/> and download the latest
version.

## Install Python on Linux
### Apt
```bash
sudo apt install python3.8
```

## How to run
### With VSCode
1. Open the .py file in vscode
2. Ensure a python 3.8 interpreter is selected (Ctrl+Shift+P > Python:Select
Interpreter > Python 3.8)
3. Run by pressing Ctrl+F5 (if you are prompted to install any modules, accept)
### From the Terminal
```bash
./[file].py
```

## How to update, build and publish

1. Ensure you have installed the following dependencies
	Linux
	```bash
	wget dephell.org/install | python3.8
	wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.8
	```
	Windows
	```powershell
	(wget dephell.org/install -UseBasicParsing).Content | python
	(wget https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
	```
2. Use poetry for the heavy lifting and dephell to generate requirements
	```bash
	poetry update
	dephell deps convert
	```
3. Build/ Publish
	```bash
	poetry build
	poetry publish
	```
	or
	```bash
	poetry publish --build
	```

## Download
### Clone
#### Using The Command Line
1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to
clone to
4. Type 'git clone' followed by URL in step 2
```bash
$ git clone https://github.com/FHPythonUtils/GimpFormats
```

More information can be found at
<https://help.github.com/en/articles/cloning-a-repository>

#### Using GitHub Desktop
1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at
<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop>

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Community Files
### Licence
LGPLv3 License
(See the [LICENSE](/LICENSE.txt) for more information.)

### Changelog
See the [Changelog](/CHANGELOG.md) for more information.

### Code of Conduct
In the interest of fostering an open and welcoming environment, we
as contributors and maintainers pledge to make participation in our
project and our community a harassment-free experience for everyone.
Please see the
[Code of Conduct](https://github.com/FHPythonUtils/.github/blob/master/CODE_OF_CONDUCT.md) for more information.

### Contributing
Contributions are welcome, please see the [Contributing Guidelines](https://github.com/FHPythonUtils/.github/blob/master/CONTRIBUTING.md) for more information.

### Security
Thank you for improving the security of the project, please see the [Security Policy](https://github.com/FHPythonUtils/.github/blob/master/SECURITY.md) for more information.
