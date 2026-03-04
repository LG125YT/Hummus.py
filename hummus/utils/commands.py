class Aliases:
    def __init__(self):
        self.aliases: dict[str, function] = {}

    def add_aliases(self, aliases: list[str]):
        def decorator(func):
            for alias in aliases:
                self.aliases[alias] = func
            return func
        return decorator


class Commands:
    def __init__(self, prefix: str, aliases: Aliases | None = None):
        from ..main import Client
        self.instance: Client | None = None
        self.prefix: str = prefix
        self.aliases: Aliases | None = aliases
