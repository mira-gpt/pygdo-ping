from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.GDT_Duration import GDT_Duration
from gdo.ping.Game import PingGame


class pong(Method):
    """Win the active ping round by being the first to answer."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'pong'

    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_execute(self) -> GDT:
        channel = self._env_channel
        user = self._env_user
        channel_id = channel.get_id() if channel else 0
        server_id = channel.get_server().get_id() if channel else 0
        user_id = user.get_id() if user else 0
        user_name = user.render_name() if user else 'Anonymous'
        result = PingGame.finish(channel_id, server_id, user_id, user_name)
        if result is None:
            return self.reply('err_pong_no_game')
        seconds, new_records = result
        duration = GDT_Duration('ping_duration').units(2, True).value(seconds).render(Application.get_mode())
        record_text = ', '.join(new_records) if new_records else 'none'
        return self.reply('msg_pong_winner', (user_name, duration, record_text))
