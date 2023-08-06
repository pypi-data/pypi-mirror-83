# dupload
Easily upload to services, get urls and automate your projects with uploads!

Version 0.0.4.2.
Fixed Starfiles API

Created by [DwifteJB](https://github.com/DwifteJB) and [CrafterPika](https://github.com/DwifteJB)

## How to install
1. Install python via your package manager or at [Python.org](https://python.org)
2. Install pip with ```python3 -m ensurepip```
3. Install this module using: ```pip install dupload```

### How to use:
```
from dupload import *
starfiles.upload("pathto/file.extension")
anonfiles.upload("pathto/file.extension")
fileio.upload("pathto/file.extension")
filepipe.upload("pathto/file.extension")

```

To gather links for further use, use this:

```
from dupload import *
link = starfiles.upload("pathto/file.extension")

print(link)
```
