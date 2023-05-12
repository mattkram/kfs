from importlib import metadata

from rich.console import Console

__version__ = metadata.version("kfs")

console = Console()
