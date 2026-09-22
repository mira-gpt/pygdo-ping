import ipaddress
import re
import subprocess

from gdo.base.GDT import GDT
from gdo.base.Method import Method
from gdo.net.GDT_Host import GDT_Host


class hping(Method):
    """Run one bounded Unix ping against a hostname or IP address."""

    LABEL = re.compile(r'^[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$')

    @classmethod
    def gdo_trigger(cls) -> str:
        return 'hping'

    def gdo_parameters(self) -> list[GDT]:
        return [GDT_Host('hostname').not_null()]

    @classmethod
    def valid_host(cls, hostname: str) -> bool:
        try:
            ipaddress.ip_address(hostname)
            return True
        except ValueError:
            pass
        hostname = hostname.rstrip('.')
        return bool(
            hostname and len(hostname) <= 253 and
            all(cls.LABEL.fullmatch(label) for label in hostname.split('.'))
        )

    @staticmethod
    def summarize(output: str) -> str:
        lines = [line.strip() for line in output.splitlines() if line.strip()]
        for line in reversed(lines):
            if line.startswith(('rtt ', 'round-trip ')) or 'time=' in line:
                return line
        return lines[-1] if lines else 'no reply'

    @classmethod
    def run_ping(cls, hostname: str) -> tuple[bool, str]:
        try:
            result = subprocess.run(
                ['/usr/bin/ping', '-n', '-c', '1', '-W', '1', '--', hostname],
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
                env={'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'},
            )
        except (OSError, subprocess.TimeoutExpired):
            return False, 'ping unavailable or timed out'
        return result.returncode == 0, cls.summarize(result.stdout or result.stderr)

    def gdo_execute(self) -> GDT:
        hostname = self.param_val('hostname')
        if not self.valid_host(hostname):
            return self.reply('err_hping_invalid_host')
        success, summary = self.run_ping(hostname)
        return self.reply('msg_hping_success' if success else 'err_hping_failed', (hostname, summary))
