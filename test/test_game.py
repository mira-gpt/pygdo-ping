import unittest
from unittest.mock import patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.date.GDT_Duration import GDT_Duration
from gdo.ping.Game import PingGame
from gdo.ping.method.hping import hping
from gdo.ping.method.ping import ping


class PingGameTest(unittest.TestCase):

    def setUp(self):
        PingGame.clear()
        Application.mode(Mode.render_cli)

    @patch.object(Application, 'request_time', return_value=0.123)
    def test_ping_uses_a_duration_value(self, _):
        duration = ping.response_duration()
        self.assertIsInstance(duration, GDT_Duration)
        self.assertEqual(0.123, duration.get_value())

    def test_first_pong_wins_and_closes_the_round(self):
        self.assertTrue(PingGame.start(53, 100.0))
        self.assertFalse(PingGame.start(53, 101.0))
        self.assertEqual(
            (0.25, ['world', 'server', 'channel', 'personal']),
            PingGame.finish(53, 12, 5, 'Gizmore', 100.25),
        )
        self.assertIsNone(PingGame.finish(53, 12, 6, 'Golden1', 100.26))

    def test_only_faster_results_replace_records(self):
        PingGame.start(53, 100.0)
        PingGame.finish(53, 12, 5, 'Gizmore', 100.25)
        PingGame.start(53, 101.0)
        self.assertEqual(
            (0.50, ['personal']),
            PingGame.finish(53, 12, 6, 'Golden1', 101.50),
        )
        self.assertEqual('Gizmore', PingGame.WORLD[0].user_name)
        self.assertEqual('Golden1', PingGame.USERS[6].user_name)

    def test_hping_accepts_hosts_but_not_shell_like_values(self):
        self.assertTrue(hping.valid_host('example.org'))
        self.assertTrue(hping.valid_host('192.0.2.1'))
        self.assertFalse(hping.valid_host('-c1'))
        self.assertFalse(hping.valid_host('example.org;id'))

    def test_hping_summary_prefers_round_trip_time(self):
        output = (
            'PING example.org (192.0.2.1) 56(84) bytes of data.\n'
            '64 bytes from 192.0.2.1: icmp_seq=1 ttl=57 time=12.3 ms\n'
            'rtt min/avg/max/mdev = 12.300/12.300/12.300/0.000 ms\n'
        )
        self.assertEqual('rtt min/avg/max/mdev = 12.300/12.300/12.300/0.000 ms', hping.summarize(output))
