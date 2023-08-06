# Starfiles API (Python)
Simplify starfiles, if it was simple already

## How to install
1. Install python via your package manager or at [Python.org](https://python.org)
2. Install pip with ```python3 -m ensurepip```
3. Install this module using: ```pip install starfiles```

### How to use:
```
import starfiles
starfiles.upload("file.extension")

```

To gather links for further use, use this:

```
import starfiles
link = starfiles.upload("pathto/file.extension")

print(link)
```
