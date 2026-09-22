from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.GDT_Duration import GDT_Duration
from gdo.ping.Game import PingGame


class records(Method):
    """Show the current Dog-run records relevant to this user and channel."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'ping.records'

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        channel = self._env_channel
        user = self._env_user
        channel_id = channel.get_id() if channel else 0
        server_id = channel.get_server().get_id() if channel else 0
        user_id = user.get_id() if user else 0
        entries = PingGame.records(server_id, channel_id, user_id)
        if not entries:
            return self.reply('msg_ping_records_empty')
        text = ', '.join(
            f'{label}: {record.user_name} ({GDT_Duration("ping_duration").units(2, True).value(record.seconds).render(Application.get_mode())})'
            for label, record in entries
        )
        return self.reply('msg_ping_records', (text,))
