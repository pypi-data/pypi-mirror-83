
import argparse
import getpass
import json
from databind.json import to_str as to_json_str
from itertools import islice
from . import ShanaProject

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username')
parser.add_argument('-p', '--password')
parser.add_argument('--follows', action='store_true')
parser.add_argument('--all', action='store_true')
parser.add_argument('-l', '--limit', type=int)
parser.add_argument('-d', '--download', type=int)
parser.add_argument('-D', '--directory')


def main():
  args = parser.parse_args()
  sp = ShanaProject()

  if not sp.load_session('main') or args.username:
    if not args.password:
      args.password = getpass.getpass('Password: ')
    sp.login(args.username, args.password)
    sp.save_session('main')

  if args.follows:
    releases = sp.follows(args.all)
    if args.limit is not None:
      releases = islice(releases, 0, args.limit)
    for release in releases:
      print(to_json_str(release))
    return

  if args.download:
    print(sp.download_release_to(args.directory or '.', args.download))
    return

  if not args.username:
    parser.print_usage()


if __name__ == '__main__':
  main()
