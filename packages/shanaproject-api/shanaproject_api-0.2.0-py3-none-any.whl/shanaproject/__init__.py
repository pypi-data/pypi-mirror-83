
__author__ = 'Fading <fading@miracle.org>'
__version__ = '0.2.0'

import os
import pickle
import posixpath
import requests
import sys
import typing as t
from urllib.parse import urljoin, unquote
from . import model, parser


class LoginError(Exception):
  pass


class ShanaProject:

  DEFAULT_USER_AGENT = f'Python/{sys.version.split()[0]} shanaproject-api ({__version__})'
  LOGIN_URL = 'https://www.shanaproject.com/login/'
  FOLLOWS_URL = 'https://www.shanaproject.com/follows/'
  SEARCH_URL = 'https://www.shanaproject.com/search/'
  IGNORE_URL = 'https://www.shanaproject.com/ajax/ignore/'
  UNIGNORE_URL = 'https://www.shanaproject.com/ajax/queue_rss/'
  DOWNLOAD_URL = 'https://www.shanaproject.com/download/'

  def __init__(self):
    self.session = requests.Session()
    self.session.headers['User-Agent'] = self.DEFAULT_USER_AGENT

  def _ajax_request(self, method: str, url: str, **kwargs: t.Any) -> requests.Response:
    headers = dict(kwargs.pop('headers', None) or {})
    headers['X-Requested-With'] = 'XMLHttpRequest'
    for cookie in self.session.cookies:
      if cookie.name.lower() == 'csrftoken':
        headers['X-CSRFToken'] = cookie.value
        break
    else:
      raise RuntimeError('no csrftoken cookie found, is this a logged in session?')
    return self.session.request(method, url, headers=headers, **kwargs)

  def _get_session_filename(self, id: str) -> str:
    filename = '~/.cache/shanaproject-api-session.{id}.pickle'
    return os.path.expanduser(filename).format(id=id)

  def save_session(self, id: str) -> None:
    filename = self._get_session_filename(id)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'wb') as fp:
      pickle.dump(self.session.cookies, fp)

  def load_session(self, id: str) -> bool:
    filename = self._get_session_filename(id)
    if os.path.isfile(filename):
      with open(filename, 'rb') as fp:
        self.session.cookies.update(pickle.load(fp))
      return True
    return False

  def login(self, username: str, password: str) -> None:
    html = self.session.get(self.LOGIN_URL).text
    csrf_token = parser.get_csrf_middleware_token(html)
    form = {'csrfmiddlewaretoken': csrf_token, 'next': '', 'username': username, 'password': password}
    response = self.session.post(self.LOGIN_URL, data=form)
    response.raise_for_status()
    error = parser.get_login_error(response.text)
    if error:
      raise LoginError(error)

  def follows(self, all_: bool = False, max_pages: int = -1) -> t.Iterable[model.Release]:
    page_num = 1
    page_url = self.FOLLOWS_URL
    if all_:
      page_url += '/all'
    while (max_pages < 0 or page_num <= max_pages) and page_url:
      html = self.session.get(page_url).text
      releases, page_url = parser.parse_search_results(html, self.FOLLOWS_URL)
      page_url = urljoin(self.FOLLOWS_URL, page_url) if page_url else None
      yield from releases

  def ignore_release(self, release_id: int) -> None:
    response = self._ajax_request('POST', self.IGNORE_URL, data={'id': release_id})
    response.raise_for_status()

  def unignore_release(self, release_id: int) -> None:
    response = self._ajax_request('POST', self.UNIGNORE_URL, data={'id': release_id})
    response.raise_for_status()

  def download_release(self, release_id: int) -> requests.Response:
    response = self.session.get(self.DOWNLOAD_URL + str(release_id))
    response.raise_for_status()
    return response

  def download_release_to(self, directory: str, release_id: int) -> str:
    " Downloads a release to the *directory* and returns the torrent filename. "

    directory = os.path.expanduser(directory)
    response = self.download_release(release_id)
    filename = posixpath.basename(unquote(response.request.url))
    filename = os.path.join(directory, filename)
    with open(filename, 'wb') as fp:
      fp.write(response.content)
    return filename

  def search(self, title: str = '', subber: str = '', max_pages: int = -1) -> t.Iterable[model.Release]:
    params = {'title': title, 'subber': subber, 'sort': 'date', 'dir': 'Descending'}
    html = self.session.get(self.SEARCH_URL, params=params).text
    page_num = 1
    while (max_pages < 0 or page_num <= max_pages):
      releases, next_page_url = parser.parse_search_results(html, self.SEARCH_URL)
      yield from releases
      if not next_page_url:
        break
      next_page_url = urljoin(self.SEARCH_URL, next_page_url)
      html = self.session.get(next_page_url).text
      page_num += 1
