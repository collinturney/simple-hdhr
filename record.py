#!/usr/bin/env python

import argparse
import os
import requests
import signal
import sys
import time
from urllib.parse import urlunparse

def channel_url(options):
    scheme = 'http'
    netloc = options.hostname or os.environ.get('HDHR_HOST')
    path = '/auto/v' + options.channel
    params = ''
    query = ''
    fragment = ''

    if not netloc:
        print("HDHR_HOST environment variable undefined.")
        print("    (e.g., export HDHR_HOST='10.10.1.100')\n")
        sys.exit(2)

    netloc += ":5004"

    return urlunparse((scheme, netloc, path, params, query, fragment))

def main(args=None):
    args = args or sys.argv[1:]

    parser = argparse.ArgumentParser()

    def configure(args):
        parser.add_argument("-H", "--hostname")
        parser.add_argument("-c", "--channel")
        parser.add_argument("-o", "--output-file")
        parser.add_argument("-m", "--minutes", type=int)

        return parser.parse_args(args)

    options = configure(args)

    done = False

    def handler(signum, frame):
        nonlocal done
        done = True
    
    signal.signal(signal.SIGALRM, handler)
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)

    signal.alarm(options.minutes * 60)

    url = channel_url(options)

    print("Recording", url, "...")

    response = requests.get(url, stream=True, timeout=3.00)
    response.raise_for_status()

    with open(options.output_file, 'wb') as fd:
        for chunk in response.iter_content(1 * 1024 * 1024):
            if done: break
            fd.write(chunk)

    response.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
