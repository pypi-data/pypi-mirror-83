# shanaproject-api

Python API for https://www.shanaproject.com/.

## Quickstart

```python
from shanaproject import ShanaProject
sp = ShanaProject()
if not sp.load_session(username):
  sp.login(username, password)
  sp.save_session(username)
for release in sp.follows():
  sp.download_release_to('~/Downloads', release.id)
```
