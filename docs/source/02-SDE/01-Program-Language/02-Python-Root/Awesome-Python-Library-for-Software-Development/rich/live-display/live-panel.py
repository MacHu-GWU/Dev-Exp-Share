import time

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
from rich.text import Text

console = Console()

with console.pager():
    panel = Panel(Text(), title="start", subtitle="end", title_align="left", subtitle_align="left")
    with Live(panel, refresh_per_second=4, screen=True):
        for ith in range(1, 1+30):
            time.sleep(1)
            panel.renderable.append(f"{ith} try ...\n")
