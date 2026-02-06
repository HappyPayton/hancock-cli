"""Interactive prompts for user input."""

from rich.prompt import Prompt, Confirm
from .colors import console


def ask_yes_no(question: str, default: bool = False) -> bool:
    """Ask a yes/no question."""
    return Confirm.ask(question, default=default, console=console)


def ask_text(question: str, default: str = None) -> str:
    """Ask for text input."""
    return Prompt.ask(question, default=default, console=console)


def ask_path(question: str, default: str = None) -> str:
    """Ask for a file path."""
    from pathlib import Path

    while True:
        path_str = Prompt.ask(question, default=default, console=console)
        path = Path(path_str).expanduser()

        if path.exists():
            return str(path.absolute())
        else:
            console.print(f"[error]✗ Path not found: {path}[/error]")
            console.print("[muted]Please enter a valid path, or press Ctrl+C to cancel[/muted]")


def ask_choice(question: str, choices: list, default: str = None) -> str:
    """Ask user to choose from a list of options."""
    return Prompt.ask(
        question,
        choices=choices,
        default=default,
        console=console
    )
