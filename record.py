#!/usr/bin/env python3

import argparse
import os
import requests
import signal
import sys
import time


def channel_url(options):
    local_ip = None

    if options.hostname:
        local_ip = options.hostname
    else:
        response = requests.get("http://ipv4-my.hdhomerun.com/discover")
        response.raise_for_status()
        data = response.json()
        local_ip = data[0]["LocalIP"]

    return "http://{}:5004/auto/v{}".format(local_ip,
                                            options.channel)


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
            if done:
                break
            fd.write(chunk)

    response.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
