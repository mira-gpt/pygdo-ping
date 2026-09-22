# pygdo-ping

`pygdo-ping` is a small PyGDO channel icebreaker.

`ping` answers in the classic form `Pong! Compliance (user) = <duration>`.

1. Start a round with `pinggame`.
2. The Dog announces `PING!`.
3. The first user to send `pong` wins; their reaction time is compared against
   world, server, channel, and personal records.

Use `ping.records` to show the relevant records. Records intentionally live in
memory for the current Dog run while the game mechanics are being tested.

## Install

Clone this repository into a PyGDO installation at `gdo/ping`, enable the
module, then reload PyGDO or restart the Dog.

The module depends on PyGDO's `date` module.

## Test

```sh
python3 -m unittest gdo.ping.test.test_game
```
