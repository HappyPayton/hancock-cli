"""Main CLI entry point for Hancock."""

import click
from . import __version__
from .ui import console


@click.group()
@click.version_option(version=__version__, prog_name="hancock")
def main():
    """
    Hancock - Gmail Signature Deployment CLI

    Deploy signatures to your entire Google Workspace from the terminal.

    \b
    Quick Start:
      1. hancock init              # Set up credentials
      2. Create signature HTML files in a folder
      3. hancock deploy signatures/  # Deploy!

    \b
    ✨ Pro tip: Run Hancock in Claude Code terminal for guided setup help!
    """
    pass


@main.command()
def init():
    """
    Interactive setup - configure Hancock for first use.

    Walks you through:
      • Service account JSON key setup
      • Google Workspace admin email
      • Credential validation

    Takes 5-15 minutes on first run.
    """
    from .commands.init import run_init
    run_init()


@main.command()
@click.argument('folder', type=click.Path(exists=True))
@click.option(
    '--dry-run',
    is_flag=True,
    help='Show what would be deployed without actually deploying'
)
def deploy(folder, dry_run):
    """
    Deploy signatures from a FOLDER to Google Workspace users.

    \b
    Example:
      hancock deploy signatures/
      hancock deploy ~/Documents/my-signatures/ --dry-run

    \b
    File Naming:
      Name your HTML files to match users:
        • john.smith.html → john.smith@company.com
        • jane-doe.html → jane.doe@company.com
        • bobsmith.html → bob.smith@company.com

    \b
    Tips:
      • Keep signatures under 10KB (Gmail limit)
      • Use base64-encoded images (no external hosting)
      • Test with --dry-run first!
    """
    from .commands.deploy import run_deploy
    run_deploy(folder, dry_run)


@main.command()
@click.argument('email')
def preview(email):
    """
    Preview the current signature for a user (EMAIL).

    \b
    Example:
      hancock preview john@company.com

    Shows the current Gmail signature HTML for the specified user.
    """
    from .commands.preview import run_preview
    run_preview(email)


@main.command()
@click.argument('folder', type=click.Path(exists=True))
def validate(folder):
    """
    Validate signature files in a FOLDER without deploying.

    \b
    Example:
      hancock validate signatures/

    Checks:
      • File size (must be under 10KB)
      • HTML format
      • Image encoding (base64 vs external)
      • Matching to users

    Use this to check your signatures before deploying.
    """
    from .commands.deploy import run_deploy
    # Validate is the same as dry-run deploy
    console.print("[bold cyan]Validating signatures...[/bold cyan]\n")
    run_deploy(folder, dry_run=True)


@main.command()
def config():
    """
    Show current Hancock configuration.

    Displays:
      • Config file location
      • Service account path
      • Admin email
      • Configuration status
    """
    from .core.config import get_config

    cfg = get_config()

    console.print("[bold cyan]Hancock Configuration[/bold cyan]\n")
    console.print(f"[bold]Config file:[/bold] {cfg.get_config_path()}")

    if cfg.exists():
        console.print(f"[bold]Service account:[/bold] {cfg.get('service_account_file', '[not set]')}")
        console.print(f"[bold]Admin email:[/bold] {cfg.get('admin_email', '[not set]')}")

        if cfg.is_configured():
            console.print("\n[green]✓ Fully configured and ready to use[/green]\n")
        else:
            console.print("\n[yellow]⚠ Configuration incomplete[/yellow]")
            console.print("[cyan]Run:[/cyan] [bold]hancock init[/bold]\n")
    else:
        console.print("\n[yellow]No configuration found[/yellow]")
        console.print("[cyan]Run:[/cyan] [bold]hancock init[/bold]\n")


if __name__ == '__main__':
    main()
