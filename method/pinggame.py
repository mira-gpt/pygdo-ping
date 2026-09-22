from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.ping.Game import PingGame


class pinggame(Method):
    """Open a channel ping round; the first pong wins."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'pinggame'

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        channel_id = self._env_channel.get_id() if self._env_channel else 0
        if not PingGame.start(channel_id):
            return self.reply('err_pinggame_active')
        return self.reply('msg_pinggame_start')
