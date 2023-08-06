# NotiaDB
*A basic database system for Python.* For download [notiadb](https://pypi.org/project/notiadb/)

[![License](https://img.shields.io/badge/license-MIT-green)](https://img.shields.io/badge/license-MIT-green)
[![Version](https://img.shields.io/badge/version-0.6-blue)](https://img.shields.io/badge/version-0.6-blue)
[![Status](https://img.shields.io/badge/status-alpha-red)](https://img.shields.io/badge/status-alpha-red)

## Quick Start

### write() and read()<br>
```py
import notiadb as db

db = db.NotiaDB("name")
name = input("Your name: ")
db.write(name=name)
print(db.read("name"))
```

### update()
```py
import notiadb as db

db = db.NotiaDB("languages", auto_id=True)
db.writeNl(name="Python")
db.writeNl(name="C")
db.update(db.filter("name", "C") name="C++")
```

### Other
```
-start_from_scratch(**kwargs): Start from scratch.
-readKeys(): Reads only keys in the file
-readValues(): Reads only values in the file
-readFile(): Reads all the file
-filter(key, value): Returns the dictionary with the desired key and value, returns a list if there is more than one
value to return
```