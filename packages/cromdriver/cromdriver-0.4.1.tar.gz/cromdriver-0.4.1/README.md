# Cromdriver
> Auto downloader for chromedriver

Cromdriver is a library to download automatically the latest Chromedriver release for Selenium.

![](docs/header.png)

Import the lib in your Selenium project and it will download and the AppData directory the latest release from [http://chromedriver.storage.googleapis.com/index.html](http://chromedriver.storage.googleapis.com/index.html).

You can get any version published in the website.

Drivers are downloaded : 

* **Mac OS X** : `~/Library/Application Support/cromdriver`
* **Unix** : `~/.local/share/cromdriver`
* **Windows** : `C:\Users\<username>\AppData\Local\cromdriver\cromdriver`

## Installation

Install the library with PIP

```sh
pip install cromdriver
```

## Usage example

There are two ways to use the library :

### Selenium python file

```python
from selenium import webdriver
import cromdriver

driver = webdriver.Chrome()
driver.get('https://www.google.com')
```

```python
import os
from selenium import webdriver
import cromdriver

path = os.path.join(cromdriver.get_chromedriver_path(), 'chromedriver.exe')

driver = webdriver.Chrome(executable_path=path)
driver.get('https://www.google.com')
```

### CLI

```console
~$ cromdriver get
Downloading version : 86.0.4240.22
Path : C:\Users\gauth\AppData\Local\cromdriver\cromdriver\RELEASE\86.0.4240.22

~$ cromdriver get --version 85.0.4183.87 --platform linux
Downloading version : 85.0.4183.87
Path : C:\Users\gauth\AppData\Local\cromdriver\cromdriver\RELEASE\85.0.4183.87
```

```console
~$ cromdriver test
Last release on your machine : 86.0.4240.22
Last release on http://chromedriver.storage.googleapis.com/index.html : 86.0.4240.22
```

```console
~$ cromdriver list
Chromedrivers downloaded :
   - 85.0.4183.87
   - 86.0.4240.22
```

```console
~$ cromdriver del --version 85.0.4183.87
Version 85.0.4183.87 deleted
```

When you use this CLI, PATH environnement variable is not updated. You will need to add the directory path to the ENV.

## Release History

* 0.4.0
    * CHANGE: Update README.md
    * ADD: Github action to deploy in Pypi
* 0.3.0
    * ADD : First working version
## Meta

Gauthier Chaty – [@gokender](https://twitter.com/gokender) – gauthier.chaty+github@outlook.com

Distributed under the MIT license. See ``LICENSE`` for more information.

[https://github.com/Gokender](https://github.com/Gokender/)
