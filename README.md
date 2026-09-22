# pygdo-ping

`pygdo-ping` is a small PyGDO module that provides the `ping` command.
It replies with `PONG` and a `GDT_Duration` rendering of the time needed to
build that response. It is intended as a lightweight basis for IRC ping games.

## Install

Clone this repository into a PyGDO installation at `gdo/ping`, enable the
module, then reload PyGDO or restart the Dog.

The module depends on PyGDO's `date` module.

## Test

```sh
python3 -m unittest gdo.ping.test.test_ping
```
