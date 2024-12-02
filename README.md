# PirateBay.py
This project is intended to be an API wrapper for [apibay](https://apibay.org/q.php?q=Example) & [ThePirateBay (only the 'main.js' file for the trackers)](https://thepiratebay.org/static/main.js)

# How does it works?
The functionality of this project is very easy to understand, as it's composed by a set of methods that point directly to the PirateBay API ([apibay](https://apibay.org/q.php?q=Example)) with the sole purpose of parsing the response for the coder to then use it.

# Installation
You can install this project by running the following commands:
```bash
pip install PirateBayAPI
# OR
pip install .
```

## A very simple example that searchs "The Tomorrow War" in the Video.Movies category and prints results
```python
import PirateBayAPI
import typing

# Static Typing isn't required (but recomended)
results: typing.List[PirateBayAPI.SearchElement] = PirateBayAPI.Search(
    "The Tomorrow War", PirateBayAPI.VideoType.Movies)

for result in results:
    print("File: {} {}.Mb (id:{})".format(
        result.name, round(result.size/1024/1024, 2), result.id))
```

## Another example, in this case, we get the magnet link (necessary to download) of the first result of the search
```python
import PirateBayAPI
import typing

# Static Typing isn't required (but recomended)
results: typing.List[PirateBayAPI.SearchElement] = PirateBayAPI.Search(
    "The Tomorrow War", PirateBayAPI.VideoType.Movies)

print("Download Link: {} (size:{}.Mb)".format(
    PirateBayAPI.Download(results[0].id), round(results[0].size/1024/1024, 2)))
```
