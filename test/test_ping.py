import unittest
from unittest.mock import patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.date.GDT_Duration import GDT_Duration
from gdo.ping.method.ping import ping


class PingTest(unittest.TestCase):

    def setUp(self):
        Application.mode(Mode.render_cli)

    @patch.object(Application, 'request_time', return_value=0.123)
    def test_response_duration_uses_gdt_duration(self, _):
        duration = ping.response_duration()
        self.assertIsInstance(duration, GDT_Duration)
        self.assertEqual(0.123, duration.get_value())
