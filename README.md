# PirateBay.py
This project is intended to be an API wrapper for [apibay](https://apibay.org/q.php?q=Example) & [ThePirateBay(only main.js for the trackers)](https://thepiratebay.org/static/main.js)

# How it works
It's own functionality is very easy to understand, its composed by a set of function's that points directly to the PirateBay API ([apibay](https://apibay.org/q.php?q=Example)) and parses the response for the programmer.

# Installation
You can install this project by running the following command's (Note: You need to have *requests* package installed)
```bash
pip install PirateBayAPI
# OR
pip install .
```

## A very simple example that search's "The Tomorrow War" in the Video.Movies category and prints result's
```python
import PirateBay
import typing

# Static Typing isn't required (but recomended)
results: typing.List[PirateBay.SearchElement] = PirateBay.Search(
    "The Tomorrow War", PirateBay.VideoType.Movies)

for result in results:
    print("File: {} {}.Mb (id:{})".format(
        result.name, round(result.size/1024/1024, 2), result.id))
```

## Another example, in this case, we get the download magnet link from the first result of the search
```python
import PirateBay
import typing

# Static Typing isn't required (but recomended)
results: typing.List[PirateBay.SearchElement] = PirateBay.Search(
    "The Tomorrow War", PirateBay.VideoType.Movies)

print("Download Link: {} (size:{}.Mb)".format(
    PirateBay.Download(results[0].id), round(results[0].size/1024/1024, 2)))
```
