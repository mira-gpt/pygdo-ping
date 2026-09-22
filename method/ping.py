from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.date.GDT_Duration import GDT_Duration


class ping(Method):
    """Reply with the command handling time for a simple IRC ping game."""

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'ping'

    def gdo_needs_authentication(self) -> bool:
        return False

    @staticmethod
    def response_duration() -> GDT_Duration:
        """Elapsed time from command receipt to the response being built."""
        return GDT_Duration('ping_duration').units(2, True).value(Application.request_time())

    def gdo_execute(self) -> GDT:
        duration = self.response_duration()
        return self.reply('msg_pong', (duration.render(Application.get_mode()),))
