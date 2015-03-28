#!/usr/bin/env python

import argparse
import json
import os
import requests
import subprocess
import sys
from urllib.parse import urlunparse


def lineup_url(options):
    scheme = 'http'
    netloc = options.hostname or os.environ.get('HDHR_HOST')
    path = '/lineup.json'
    params = ''
    query = ''
    fragment = ''

    if not netloc:
        print("HDHR_HOST environment variable undefined.")
        print("    (e.g., export HDHR_HOST='10.10.1.100')\n")
        sys.exit(2)

    return urlunparse((scheme, netloc, path, params, query, fragment))

def print_lineup(lineup):
    for channel in lineup:
        print("{GuideNumber},{GuideName},{URL}".format(**channel))

def watch_channel(lineup, target):
    for channel in lineup:
        if channel['GuideNumber'] == target:
            playlist = [channel['URL'] for channel in lineup]
            subprocess.call(['vlc', channel['URL']] + playlist)
            break
    else:
        print("Channel '%s' not found in lineup" % target)

def main(args=None):
    args = args or sys.argv[1:]

    parser = argparse.ArgumentParser()

    def configure(args):
        parser.add_argument('-H', '--hostname')
        parser.add_argument('-c', '--channel')
        parser.add_argument('-l', '--list-channels', action='store_true')

        return parser.parse_args(args)

    options = configure(args)

    response = requests.get(lineup_url(options), timeout=3.00)
    lineup = json.loads(response.text)

    if options.list_channels:
        print_lineup(lineup)
        return 0
    elif options.channel:
        watch_channel(lineup, options.channel)
        return 0
    else:
        parser.print_help()
        return 2

if __name__ == "__main__":
    sys.exit(main())
