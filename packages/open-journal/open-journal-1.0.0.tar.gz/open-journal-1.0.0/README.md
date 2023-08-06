# open-journal
A simple, private, open-source journal for Linux. No user data is collected.

### Encryption
Journals can be optionally encrypted using a uniquely generated encryption key. The *cryptography* library used is built on AES. The encryption key only needs to be generated once. Export a copy of it from the program and store it in a safe place. 

The encryption key must be stored in the same location as **Open-Journal.py** or the executable. It is placed here automatically upon generation.

### Prerequisites 
In order to run Open Journal, you must have the prerequisites defined in **requirements.txt** installed in your environment.

To install *PyQt5*, run one of the following commands:
~~~
pip install pyqt5
~~~

or

~~~
pip3 install pyqt5
~~~

To install *cryptography*:
~~~
pip3 install cryptography
~~~

### Installation and Usage
To install and use Open Journal, choose one of the following options.

1.) Clone the repository to your computer and run **Open-Journal.py** from your terminal. Alternatively, run it from an IDE of your choice, such as PyCharm.
~~~
$ python Open-Journal.py
~~~

2.) You can download the executable from the *releases* page. It was built using PyInstaller and Python 3.6.12.

Open Journal was developed and tested on Linux (Ubuntu 20.04.1 LTS). However, if you have all requirements met, you should have no issue running it on Windows or MacOS. At least, in its Python form.

### Building from source
If you wish to build an executable yourself from the source code provided you can do so as outlined here.

1.) Install PyInstaller into your environment that has the prerequisites. I highly recommend making a Conda environment with those packages installed and using Python 3.6 for best results. Switch to that environment in your terminal and run the following command.
~~~
pip install pyinstaller
~~~

2.) Create a spec file in the root project directory by running the following command that will use --onefile mode, to include all files in a single executable.
~~~
pyi-makespec --onefile Open-Journal.py
~~~

Add the following lines of code to the beginning of the **Open-Journal.spec** file. If you do not, you will likely encounter a recursion error.
~~~
# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(5000)
~~~

3.) Build the executable.
~~~
pyinstaller Open-Journal.spec
~~~
A *build* and *dist* folder will be created. The executable is located under *dist* with the name **Open-Journal**.

### Screenshots
![Main Menu](/screenshots/open-journal.png)

### License

Copyright (C) 2020 Stuart Clayton

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
