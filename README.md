## What does this Python Script do?
https://wiki.archlinux.org/index.php/XDG_Base_Directory 
Uses the tables of file paths on this site to see if you have any files using legacy paths.

## Dependencies
BeautifulSoup
```
$ pip install requests BeautifulSoup4
```

Python3


## How to use
```
$ python dotdot.py
```
Will return a list of files that are using legacy paths.
See: https://wiki.archlinux.org/index.php/XDG_Base_Directory

