Simple HDHR
===========

Scripts to browse, view, and record video streams from a [HDHomeRun](http://www.silicondust.com) device.

## View and Browse

### Usage

    $ ./watch.py -h
    usage: watch.py [-h] [-u URL] [-c CHANNEL] [-l]

    optional arguments:
      -h, --help            show this help message and exit
      -c CHANNEL, --channel CHANNEL
      -l, --list-channels

### Examples

List lineup data:

    $ watch.py -l
    2.1,KETS-1,http://10.10.1.100:5004/auto/v2.1
    2.2,KETS-2,http://10.10.1.100:5004/auto/v2.2
    2.3,KETS-3,http://10.10.1.100:5004/auto/v2.3
    2.4,KETS-4,http://10.10.1.100:5004/auto/v2.4
    4.1,KARK-DT,http://10.10.1.100:5004/auto/v4.1
    7.1,KATV-HD,http://10.10.1.100:5004/auto/v7.1
    7.2,RTV,http://10.10.1.100:5004/auto/v7.2
    7.3,GRIT,http://10.10.1.100:5004/auto/v7.3
    11.1,KTHV-DT,http://10.10.1.100:5004/auto/v11.1
    11.2,THV2,http://10.10.1.100:5004/auto/v11.2
    11.3,Justice,http://10.10.1.100:5004/auto/v11.3
    16.1,KLRT-DT,http://10.10.1.100:5004/auto/v16.1
    20.1,KLRA-CD,http://10.10.1.100:5004/auto/v20.1
    30.1,KKYK-CD,http://10.10.1.100:5004/auto/v30.1
    30.2,KKYK-CD,http://10.10.1.100:5004/auto/v30.2
    30.3,KKYK-CD,http://10.10.1.100:5004/auto/v30.3
    30.4,KKYK-CD,http://10.10.1.100:5004/auto/v30.4
    36.1,KKAP-DT,http://10.10.1.100:5004/auto/v36.1
    38.1,KASN-HD,http://10.10.1.100:5004/auto/v38.1
    42.1,KARZ-DT,http://10.10.1.100:5004/auto/v42.1
    42.2,BOUNCE,http://10.10.1.100:5004/auto/v42.2
    49.1,KMYA-DT,http://10.10.1.100:5004/auto/v49.1
 
View channel 7.1 using VLC:

    $ watch.py -c 7.1

## Record

### Usage

    $ record.py -h
    usage: record.py [-h] [-u URL] [-o OUTPUT_FILE] [-m MINUTES]

    optional arguments:
      -h, --help            show this help message and exit
      -c CHANNEL, --channel CHANNEL
      -o OUTPUT_FILE, --output-file OUTPUT_FILE
      -m MINUTES, --minutes MINUTES

### Examples

Record channel 11.1 for 30 minutes:

    $ record.py -c 11.1 -o output.mpg -m 30

Record the nightly news using cron:

    30 17 * * * record.py -c 7.1 -o news.mpg -m 30

