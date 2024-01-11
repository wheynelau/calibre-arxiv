# calibre-arxiv

## Description

This is a plugin for [Calibre](http://calibre-ebook.com/) that allows you to
download metadata and covers for papers from [arXiv](http://arxiv.org/).

This project was initially developed to assist in managing academic papers within Calibre, tailored to my needs. As such, it may not encompass all the features that could be beneficial to a wider audience. I am actively seeking feedback and suggestions to enhance its functionality and user experience.

## Installation

### Release files
1. Download the latest release from the [releases page](https://github.com/wheynelau/calibre-arxiv/releases).
2. Upload the plugin to calibre by Preferences -> Plugins -> Load Plugin from File and select the zip file you downloaded.
3. There should be an option to restart calibre after installation. If not, restart calibre manually.
4. The plugin should now be installed and ready to use.


### Source files
1. Clone the repository.
2. Run `bash ./zip.sh` or manually zip these files, it must be a __zip__ file and not a rar file:
   -  `__init__.py`
   -  `main.py`
   -  `xmltodict.py`
   -  `plugin-import-name-arxiv.txt`
3. Foloow steps 2-4 in the Release files section.

## Features

### What works
- Searching by title name and downloading
- Opening of the paper's abstract page in the browser

### To be implemented
- Searching by author name
- Searching by arXiv ID
- Searching of categories
- Auto downloads of papers using RSS or other methods (is this done within calibre?)

## Contributing

Feel free to raise issues and submit pull requests. I will try to respond to them as soon as possible.
