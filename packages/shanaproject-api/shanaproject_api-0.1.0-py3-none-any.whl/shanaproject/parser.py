
import bs4
import datetime
import re
import typing as t
from urllib.parse import urljoin
from . import model


def get_csrf_middleware_token(html: str) -> str:
  " Find the CSRF token from the login form. "

  soup = bs4.BeautifulSoup(html, 'html.parser')
  input_el = soup.find('input', {'type': 'hidden', 'name': 'csrfmiddlewaretoken'})
  return input_el['value']


def parse_search_results(html: str, base_url: str) -> t.Tuple[t.List[model.Release], t.Optional[str]]:
  """
  Parses the HTML page of the ShanaProject search results page. Returns the parsed releases as
  well as the URL to the next page, if present.
  """

  soup = bs4.BeautifulSoup(html, 'html.parser')

  releases = []
  for i, release_block in enumerate(soup.find_all('div', {'class': 'release_block'})):
    if i == 0: continue
    release = _parse_release_block(release_block)
    release.torrent_link = urljoin(base_url, release.torrent_link)
    releases.append(release)

  list_next = soup.find('div', {'class': 'list_next'}).find('a')
  next_page_url = list_next['href'] if list_next else None

  return releases, next_page_url


def _parse_date_string(ds: str) -> datetime.datetime:
  " Parse a date string like `Aug. 11, 2019, 2:08 a.m.`. "

  match = re.match(r'(\w+)\.?\s+(\d+),\s+(\d+),\s+(\d+):(\d+)\s+(a\.m\.|p\.m\.)', ds)
  if not match:
    raise ValueError(f'unable to parse date string: {ds!r}')

  abbreviated_months = [
    'Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

  month = abbreviated_months.index(match.group(1)) + 1
  day = int(match.group(2))
  year = int(match.group(3))
  hour = int(match.group(4))
  minute = int(match.group(5))
  half_of_day = match.group(6)
  if half_of_day == 'p.m.':
    hour = (hour + 12) % 24

  return datetime.datetime(year, month, day, hour, minute, 0)


def _parse_release_block(release_block: bs4.Tag) -> model.Release:
  series_link = (release_block
    .find('div', {'class': 'release_title'})
    .find('div', {'class': 'release_text_contents'})
    .find('a'))
  title = series_link.text
  series_id = int(re.match(r'/series/(\d+)/', series_link['href']).group(1))

  subber_link = (release_block
    .find('div', {'class': 'release_subber'})
    .find('div', {'class': 'release_text_contents'})
    .find('a'))
  subber_name = subber_link.text or None
  subber_id = int(re.match(r'/subbertag/(\d+)/', subber_link['href']).group(1)) if subber_name else None

  episode_text = release_block.find('div', {'class': 'release_episode'}).text
  match = re.match(r'(\d+)(?:v(\d+))?', episode_text)
  if match:
    episode = int(match.group(1))
    version = int(match.group(2)) if match.group(2) else None
  else:
    episode = None
    version = None

  quality_prefix = release_block.find(lambda t: t.name == 'b' and t.text == 'Quality:')
  quality = quality_prefix.next_sibling.strip()
  date_string = quality_prefix.parent.find_next_sibling('div', {'class': 'release_last'}).text.strip()
  date = _parse_date_string(date_string)
  extension_prefix = release_block.find(lambda t: t.name == 'b' and t.text == 'Extension:')
  extension = extension_prefix.next_sibling.strip()
  filename = extension_prefix.parent.find_next_sibling('div', {'class': 'release_original'}).text.strip()
  comment_div = release_block.find('div', {'class': 'release_comment_text'})
  comment = comment_div.text.strip() if comment_div else None
  profiles = [x.text for x in release_block.find_all('span', {'class': 'release_profile'})]
  size = release_block.find('div', {'class': 'release_size'}).text
  torrent_link = (
    release_block.find('div', {'class': 'release_download'}) or
    release_block.find('div', {'class': 'release_download_mini'})
  ).parent['href']

  return model.Release(
    int(release_block['id'][3:]),
    model.Subber(subber_id, subber_name) if subber_name else None,
    model.Series(series_id, title),
    episode,
    version,
    model.VideoInfo(extension, filename, quality, profiles, date, comment, size),
    torrent_link)
