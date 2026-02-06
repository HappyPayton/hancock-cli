"""Terminal colors and styling using Rich."""

from rich.console import Console
from rich.theme import Theme
from rich.panel import Panel
from rich.text import Text

# Custom theme for Hancock
hancock_theme = Theme({
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "info": "bold cyan",
    "prompt": "bold magenta",
    "highlight": "bold blue",
    "muted": "dim",
})

# Global console instance
console = Console(theme=hancock_theme)


def print_success(message: str):
    """Print a success message with checkmark."""
    console.print(f"✓ {message}", style="success")


def print_error(message: str):
    """Print an error message with X."""
    console.print(f"✗ {message}", style="error")


def print_warning(message: str):
    """Print a warning message with warning icon."""
    console.print(f"⚠ {message}", style="warning")


def print_info(message: str):
    """Print an info message."""
    console.print(f"ℹ {message}", style="info")


def print_header(title: str, subtitle: str = None):
    """Print a beautiful header panel."""
    content = f"[bold]{title}[/bold]"
    if subtitle:
        content += f"\n\n{subtitle}"

    panel = Panel(
        content,
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(panel)
    console.print()


def print_section(title: str):
    """Print a section divider."""
    console.print(f"\n[bold cyan]{title}[/bold cyan]")
    console.print()
