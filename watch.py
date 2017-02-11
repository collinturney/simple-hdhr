#!/usr/bin/env python3

import argparse
import json
import os
import requests
import subprocess
import sys


def lineup_url(options):
    if options.hostname:
        return "http://{}/lineup.json".format(options.hostname)
    else:
        response = requests.get("http://ipv4-my.hdhomerun.com/discover")
        response.raise_for_status()
        data = response.json()
        return data[0]["LineupURL"]


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
