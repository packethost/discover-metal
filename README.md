# Equinix Discover Metal

[![Build Status](https://cloud.drone.io/api/badges/packethost/discover-metal/status.svg?ref=refs/heads/main)](https://cloud.drone.io/packethost/discover-metal) ![](https://img.shields.io/badge/Stability-Experimental-red.svg)

This is a tool which is used within [OSIE](https://github.com/tinkerbell/osie)
to discover components and do some initial configuration when new hardware is
brought online.

This repository is [Experimental](https://github.com/packethost/standards/blob/master/experimental-statement.md)
meaning that it's based on untested ideas or techniques and not yet established
or finalized or involves a radically new and innovative style! This means that
support is best effort (at best!) and we strongly encourage you to NOT use this
in production.

## Requirements

- [packet-hardware](https://github.com/packethost/packet-hardware#Requirements) for hardware discovery
- `lldpd` for discovering lldp information

## Installation

```shell
pip3 install git+https://github.com/packethost/discover-metal.git@main
```

## Usage

```shell
$ discover-metal --help
Usage: discover-metal [OPTIONS]

Options:
  -s, --send TEXT  Send the data to this location
  -q, --quiet      Provide more detailed output
  -v, --verbose    Provide more detailed output
  --help           Show this message and exit.
```

## Docker Usage

```shell
$ docker run --rm --net host --privileged \
    -v /dev:/dev \
    -v /sys:/sys \
    -v /tmp:/tmp \
    quay.io/packet/discover-metal:latest --help
Usage: discover-metal [OPTIONS]

Options:
  -s, --send TEXT  Send the data to this location
  -q, --quiet      Provide more detailed output
  -v, --verbose    Provide more detailed output
  --help           Show this message and exit.
```

## Sending data

when using the `-s` or `--send` option, after the script completes, it sends the
resulting json in a POST request to the specified address.

## Example output

discover-metal wraps [packet-hardware](https://github.com/packethost/packet-hardware)
The json listed below is also what you would be sent when using `-s/--send` flag.

```json
# docker run --rm --net host --privileged \
    -v /dev:/dev \
    -v /sys:/sys \
    -v /tmp:/tmp \
    quay.io/packet/discover-metal:latest
cmd="lshw -xml -quiet -disable fb", klass="utils", method="cmd_output"
...
ERROR:root:Exception occured while running module: DiscoverLLDP
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/discovermetal/discover.py", line 33, in run_module
    return module.run(self.data)
  File "/usr/local/lib/python3.5/dist-packages/discovermetal/modules/discover_lldp.py", line 58, in run
    raise TimeoutError("Timedout waiting for lldp")
TimeoutError: Timedout waiting for lldp

{
  "stats": {
    "stop": "2020-10-14T19:15:32.429879Z",
    "start": "2020-10-14T19:14:30.470350Z",
    "logs": [
      {
        "message": "Discovery Started",
        "time": "2020-10-14T19:14:30.470358Z",
        "data": {},
        "level": "INFO"
      },
      {
        "message": "[DiscoverComponents]: Started",
        "time": "2020-10-14T19:14:30.470366Z",
        "data": {},
        "level": "DEBUG"
      },
      {
        "message": "[DiscoverComponents]: Completed",
        "time": "2020-10-14T19:14:32.239628Z",
        "data": {},
        "level": "DEBUG"
      },
      {
        "message": "[DiscoverLLDP]: Started",
        "time": "2020-10-14T19:14:32.239651Z",
        "data": {},
        "level": "DEBUG"
      },
      {
        "message": "No lldp data returned, trying again in 5 seconds",
        "time": "2020-10-14T19:14:32.277327Z",
        "data": {
          "started": 1602702872.2403471,
          "current": 1602702872.2773197
        },
        "level": "DEBUG"
      },
      {
        "message": "No lldp data returned, trying again in 5 seconds",
        "time": "2020-10-14T19:14:37.290574Z",
        "data": {
          "started": 1602702872.2403471,
          "current": 1602702877.2905688
        },
        "level": "DEBUG"
      },
      {
        "message": "Exception occured while running module: DiscoverLLDP",
        "time": "2020-10-14T19:15:32.429410Z",
        "traceback": "Traceback (most recent call last):\n  File \"/usr/local/lib/python3.5/dist-packages/discovermetal/discover.py\", line 33, in run_module\n    return module.run(self.data)\n  File \"/usr/local/lib/python3.5/dist-packages/discovermetal/modules/discover_lldp.py\", line 58, in run\n    raise TimeoutError(\"Timedout waiting for lldp\")\nTimeoutError: Timedout waiting for lldp\n",
        "data": {},
        "level": "ERROR"
      },
      {
        "message": "[DiscoverLLDP]: Completed",
        "time": "2020-10-14T19:15:32.429870Z",
        "data": {},
        "level": "DEBUG"
      },
      {
        "message": "Discovery Finished",
        "time": "2020-10-14T19:15:32.429906Z",
        "data": {},
        "level": "INFO"
      }
    ]
  },
  "components": [
    {
      "name": "Unknown",
      "type": "ChassisComponent",
      "firmware_version": "",
      "serial": "C813MLJ12NG0385",
      "model": "CSE-813MFTS-R407CBP",
      "vendor": "Unknown",
      "data": {}
    },
    ...
    {
      "name": "X11SCM-F",
      "type": "MotherboardComponent",
      "firmware_version": "1.4",
      "serial": "WM206S010127",
      "model": "X11SCM-F",
      "vendor": "Supermicro",
      "data": {
        "uuid": "001039FD-29B2-EA11-8000-3CECEF6D9A12",
        "date": "05/26/2020"
      }
    }
  ]
}
```
