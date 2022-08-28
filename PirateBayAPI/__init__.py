"""
Copyright (c) 2022 Boris (x93)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import dataclasses
import datetime
import requests
import typing
import html
import enum
import re


trackers: typing.Optional[typing.List[str]] = None
trackers_re: str = "function print_trackers\(\){let ([^}]*)return tr;}"


class PirateBayError(Exception):
    pass


class AudioType(enum.Enum):
    All: int = 0

    Music: int = 1
    AudioBooks: int = 2
    SoundClips: int = 3
    FLAC: int = 4
    Other: int = 99

    BaseNO: int = 100


class VideoType(enum.Enum):
    All: int = 0

    Movies: int = 1
    MoviesDVDR: int = 2
    MusicVideos: int = 3
    MovieClips: int = 4
    TVShows: int = 5
    Handheld: int = 6
    HDMovies: int = 7
    HDTVShows: int = 8
    _3D: int = 9
    Other: int = 99

    BaseNO: int = 200


class ApplicationsType(enum.Enum):
    All: int = 0

    Windows: int = 1
    Mac: int = 2
    Unix: int = 3
    Handheld: int = 4
    IOS: int = 5
    Android: int = 6
    Other: int = 99

    BaseNO: int = 300


class GamesType(enum.Enum):
    All: int = 0

    PC: int = 1
    Mac: int = 2
    PSx: int = 3
    XBox360: int = 4
    Wii: int = 5
    Handheld: int = 6
    IOS: int = 7
    Android: int = 8
    Other: int = 99

    BaseNO: int = 400


class PornType(enum.Enum):
    All: int = 0

    Movies: int = 1
    MoviesDVDR: int = 2
    Pictures: int = 3
    Games: int = 4
    HDMovies: int = 5
    MovieClips: int = 6
    Other: int = 99

    BaseNO: int = 500


class OtherType(enum.Enum):
    All: int = 0

    EBooks: int = 1
    Comics: int = 2
    Pictures: int = 3
    Covers: int = 4
    Physibles: int = 5
    Other: int = 99

    BaseNO: int = 600


@dataclasses.dataclass
class SearchElement:
    id: int
    name: str
    info_hash: str
    leechers: int
    seeders: int
    num_files: int
    size: int
    username: str
    added: datetime.datetime
    status: str
    category: int
    imdb: str


@dataclasses.dataclass
class Torrent:
    id: int
    category: int
    status: str
    name: str
    num_files: int
    size: int
    seeders: int
    leechers: int
    username: str
    added: datetime.datetime
    descr: str
    imdb: str
    language: str
    textlanguage: str
    info_hash: str


def FetchTrackers() -> typing.List[str]:
    """
    Fetchs trackers and stores them into
     trackers variable for speed

    @return: trackers list
    """

    global trackers
    if not trackers:
        script: str = \
            requests.get("https://thepiratebay.org/static/main.js").text

        function: str = re.findall(trackers_re, script)[0]
        temp: str = function.replace("tr+='&tr='+", "")
        temp = temp.replace("encodeURIComponent('", "")
        temp = temp.replace("tr='&tr='+", "")
        temp = temp.replace("')", "")
        temp = temp[:len(temp)-1]

        trackers = temp.split(";")

    return trackers


def Trackers2String() -> str:
    """
    Parses trackers list and returns an string

    @return: trackers args
    """

    while trackers is None:
        FetchTrackers()

    out: str = ""
    for tracker in trackers:
        out += "&tr=" + html.escape(tracker)

    return out


def Search(
    query: str, ctype: typing.Optional[typing.Union[int, enum.Enum]] = None) \
        -> typing.List[SearchElement]:
    """
    Searchs into PirateBay

    @param query: Query text
    @param ctype: Type of query
    @return: SearchElement object
    """

    sctype: int = 1
    if isinstance(ctype, int):
        sctype = ctype

    elif isinstance(ctype, enum.Enum):
        sctype = type(ctype).BaseNO.value + ctype.value

    data: requests.Response = requests.get("https://apibay.org/q.php", params={
        "q": query,
        "cat": sctype
    })

    if data.status_code != 200:
        raise PirateBayError

    out: typing.List[SearchElement] = []
    for elem in data.json():
        out.append(SearchElement(
            int(elem["id"]), elem["name"],
            elem["info_hash"], int(elem["leechers"]),
            int(elem["seeders"]), int(elem["num_files"]),
            int(elem["size"]), elem["username"],
            datetime.datetime.fromtimestamp(int(elem["added"])),
            elem["status"], int(elem["category"]),
            elem["imdb"]
        ))

    return out


def GetFiles(file_id: int) \
        -> typing.Tuple[int, typing.List[typing.Tuple[str, int]]]:
    """
    Fetch's filelist from PirateBay using its file_id

    @param file_id: The id of the file
    @return: (total_size, [(size, name)...])
    """

    data: requests.Response = requests.get(
        "https://apibay.org/f.php", params={"id": file_id})

    if data.status_code != 200:
        raise PirateBayError

    total: int = 0
    files: typing.List[typing.Tuple[str, int]] = []

    for file in data.json():
        if file.get("name").get("0"):
            # FileList not found error
            return (0, [])

        total += int(file["size"][0])
        files += [(file["name"][0], int(file["size"][0]))]

    return (total, files)


def GetTorrentInfo(file_id: int) -> Torrent:
    """
    Gets torrent information

    @param file_id: The id of the file
    @return: Torrent object
    """
    data: requests.Response = requests.get(
        "https://apibay.org/t.php", params={"id": file_id})
    
    if data.status_code != 200:
        raise PirateBayError
    
    t: typing.Dict[str, typing.Any] = data.json()
    return Torrent(
        int(t["id"]), int(t["category"]),
        t["status"], t["name"], int(t["num_files"]),
        int(t["size"]), int(t["seeders"]),
        int(t["leechers"]), t["username"],
        datetime.datetime.fromtimestamp(int(t["added"])),
        t["descr"], t["imdb"], t["language"],
        t["textlanguage"], t["info_hash"]
    )


def Download(file_id: int) -> str:
    """
    Generates magnet url using PirateBay
     trackers and info_hash & name of the file

    @param file_id: The id of the file
    @return: magnet url
    """

    info: Torrent = GetTorrentInfo(file_id)
    return "magnet:?xt=urn:btih:{}&dn={}{}".format(
        info.info_hash, html.escape(info.name), Trackers2String())
