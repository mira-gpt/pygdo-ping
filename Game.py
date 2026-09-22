from dataclasses import dataclass
from time import monotonic


@dataclass(frozen=True)
class PingRecord:
    seconds: float
    user_name: str


class PingGame:
    """In-memory rounds and records for the current Dog run."""

    ROUNDS: dict[int, float] = {}
    WORLD: dict[int, PingRecord] = {}
    SERVERS: dict[int, PingRecord] = {}
    CHANNELS: dict[int, PingRecord] = {}
    USERS: dict[int, PingRecord] = {}

    @classmethod
    def clear(cls):
        cls.ROUNDS = {}
        cls.WORLD = {}
        cls.SERVERS = {}
        cls.CHANNELS = {}
        cls.USERS = {}

    @classmethod
    def start(cls, channel_id: int, now: float | None = None) -> bool:
        if channel_id in cls.ROUNDS:
            return False
        cls.ROUNDS[channel_id] = monotonic() if now is None else now
        return True

    @classmethod
    def finish(cls, channel_id: int, server_id: int, user_id: int, user_name: str, now: float | None = None) -> tuple[float, list[str]] | None:
        started = cls.ROUNDS.pop(channel_id, None)
        if started is None:
            return None
        seconds = (monotonic() if now is None else now) - started
        record = PingRecord(seconds, user_name)
        new_records = []
        for label, records, key in (
            ('world', cls.WORLD, 0),
            ('server', cls.SERVERS, server_id),
            ('channel', cls.CHANNELS, channel_id),
            ('personal', cls.USERS, user_id),
        ):
            previous = records.get(key)
            if previous is None or seconds < previous.seconds:
                records[key] = record
                new_records.append(label)
        return seconds, new_records

    @classmethod
    def records(cls, server_id: int, channel_id: int, user_id: int) -> list[tuple[str, PingRecord]]:
        records = []
        for label, record in (
            ('world', cls.WORLD.get(0)),
            ('server', cls.SERVERS.get(server_id)),
            ('channel', cls.CHANNELS.get(channel_id)),
            ('personal', cls.USERS.get(user_id)),
        ):
            if record:
                records.append((label, record))
        return records
