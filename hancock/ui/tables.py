"""Beautiful tables for displaying data."""

from rich.table import Table
from rich.text import Text
from .colors import console


def create_match_table(matches: list, unmatched: list = None, errors: list = None) -> Table:
    """Create a table showing file-to-user matches."""
    table = Table(
        title="Deployment Preview",
        show_header=True,
        header_style="bold cyan",
        border_style="cyan",
        title_style="bold",
    )

    table.add_column("Status", style="bold", width=3)
    table.add_column("File", style="")
    table.add_column("", style="muted", width=3)
    table.add_column("User", style="")

    # Add matched files
    for match in matches:
        table.add_row(
            "✓",
            match.get("filename", ""),
            "→",
            match.get("email", ""),
            style="success"
        )

    # Add unmatched files
    if unmatched:
        for file in unmatched:
            table.add_row(
                "⚠",
                file.get("filename", ""),
                "→",
                "No match found",
                style="warning"
            )

    # Add errors
    if errors:
        for error in errors:
            table.add_row(
                "✗",
                error.get("filename", ""),
                "→",
                error.get("error", "Error"),
                style="error"
            )

    return table


def print_summary(matched: int, unmatched: int, errors: int):
    """Print a summary of the deployment."""
    parts = []

    if matched > 0:
        parts.append(f"[success]{matched} ready[/success]")
    if unmatched > 0:
        parts.append(f"[warning]{unmatched} warnings[/warning]")
    if errors > 0:
        parts.append(f"[error]{errors} errors[/error]")

    summary = " • ".join(parts) if parts else "[muted]No files found[/muted]"
    console.print(f"\n{summary}\n")


def print_deployment_summary(successful: int, failed: int, skipped: int):
    """Print a summary after deployment."""
    console.print()
    if successful > 0:
        console.print(f"[success]✓ Successfully deployed {successful} signatures[/success]")
    if skipped > 0:
        console.print(f"[warning]⚠ {skipped} files skipped (no match)[/warning]")
    if failed > 0:
        console.print(f"[error]✗ {failed} files failed[/error]")
    console.print()
