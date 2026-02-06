"""Progress bars and spinners."""

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)
from .colors import console


def create_progress_bar():
    """Create a progress bar for deployment."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(complete_style="success", finished_style="success"),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def create_spinner(text: str = "Working..."):
    """Create a simple spinner."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        console=console,
        transient=True,  # Remove when done
    )
