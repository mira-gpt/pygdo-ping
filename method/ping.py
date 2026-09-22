from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.GDT_Duration import GDT_Duration


class ping(Method):
    """Reply with a measured compliance time, like classic IRC ping bots."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'ping'

    def gdo_needs_authentication(self) -> bool:
        return False

    @staticmethod
    def response_duration() -> GDT_Duration:
        return GDT_Duration('ping_duration').units(2, True).value(Application.request_time())

    def gdo_execute(self) -> GDT:
        user_name = self._env_user.render_name() if self._env_user else 'Anonymous'
        duration = self.response_duration().render(Application.get_mode())
        return self.reply('msg_ping_compliance', (user_name, duration))
