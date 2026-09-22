from gdo.base.GDO_Module import GDO_Module


class module_ping(GDO_Module):
    """Response-time ping command, kept separate from the core module."""

    def gdo_dependencies(self) -> list:
        return ['date']
