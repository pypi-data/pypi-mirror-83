# shanaproject-api

Python API and CLI for https://www.shanaproject.com/.

## Example: Download all unread follows

    $ shanaproject -u <username> -p <password>
    $ shanaproject --follows > follows.json
    $ cat follows.json | jq .id | xargs -P2 -n1 shanaproject -D follows/ -d

Let's go through the commands step by step:

1. Log into your ShanaProject account. The session will be saved in your `~/.cache` directory.
2. Download all of your unread follows into a JSON file called `follows.json`
3. For each of your follows, grab the release ID and pass it into the download command. Two
   follows will be downloaded in parallel any given point in time (`-P2`).

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
