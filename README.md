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