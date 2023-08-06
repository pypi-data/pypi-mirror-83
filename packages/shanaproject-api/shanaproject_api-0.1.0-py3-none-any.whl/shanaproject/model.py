
import datetime
import enum
import typing as t
from dataclasses import dataclass


@dataclass
class Series:
  " Represents the series that a release belongs to. "

  id: int
  title: str


@dataclass
class Subber:
  " Represents information on the subber that produced a release. "

  id: int
  name: str


@dataclass
class VideoInfo:
  extension: str
  filename: str
  quality: str
  profiles: t.List[str]
  date: datetime.datetime
  comment: str
  size: t.Optional[str]


@dataclass
class Release:
  " Represents a release. "

  id: int
  subber: t.Optional[Subber]
  series: Series
  episode: t.Optional[int]
  version: t.Optional[int]
  video: VideoInfo
  torrent_link: str
