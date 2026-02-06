"""Interactive setup command for Hancock."""

from pathlib import Path
from ..core.config import get_config
from ..core.auth import validate_credentials
from ..ui import (
    console,
    print_header,
    print_success,
    print_error,
    print_info,
    print_section,
    ask_yes_no,
    ask_text,
    ask_path,
    create_spinner,
)


def run_init():
    """Run interactive setup for Hancock."""

    print_header(
        "🎯 Hancock - Gmail Signature Deployment CLI",
        "Let's get you set up! (5-15 minutes)"
    )

    config = get_config()

    # Check if already configured
    if config.is_configured():
        console.print("[yellow]Hancock is already configured![/yellow]\n")
        console.print(f"[muted]Config file: {config.get_config_path()}[/muted]")
        console.print(f"[muted]Service account: {config.get_service_account_path()}[/muted]")
        console.print(f"[muted]Admin email: {config.get_admin_email()}[/muted]\n")

        if not ask_yes_no("Do you want to reconfigure?", default=False):
            console.print("\n[cyan]You're all set! Try: [bold]hancock deploy signatures/[/bold][/cyan]\n")
            return

        console.print()

    # Step 1: Service Account JSON
    print_section("🔐 Service Account Setup")

    console.print("[cyan]Your Google Cloud service account allows Hancock to deploy signatures\nacross your entire Google Workspace.[/cyan]\n")

    has_key = ask_yes_no("Do you already have a Google Cloud service account JSON key?", default=False)
    console.print()

    if not has_key:
        # Guide them through setup
        console.print("[yellow]No problem! Let's create one together.[/yellow]\n")

        console.print("[bold]Follow these steps:[/bold]")
        console.print("  1. Go to: [link=https://console.cloud.google.com]https://console.cloud.google.com[/link]")
        console.print("  2. Create a new project (or select existing)")
        console.print("  3. Enable [bold]Admin SDK API[/bold] and [bold]Gmail API[/bold]")
        console.print("  4. Create a service account with domain-wide delegation")
        console.print("  5. Download the JSON key file\n")

        console.print("[muted]For detailed instructions, see:[/muted]")
        console.print("[muted]https://github.com/HappyPayton/hancock-cli#-service-account-setup[/muted]\n")

        console.print("[green]✨ Pro tip:[/green] [cyan]If you're using Claude Code, Claude can help you\nthrough the Google Cloud setup![/cyan]\n")

        input("[bold]Press Enter when you have downloaded your JSON key file...[/bold]")
        console.print()

    # Get service account file path
    console.print("[bold]Where is your service account JSON file?[/bold]")
    console.print("[muted]Tip: You can drag the file into the terminal to paste the path[/muted]\n")

    service_account_path = ask_path("Service account file path")
    console.print()

    # Step 2: Admin Email
    print_section("👤 Admin Email")

    console.print("[cyan]Enter the email address of a Google Workspace super admin.\nThis account is used for domain-wide delegation.[/cyan]\n")

    admin_email = ask_text("Google Workspace admin email")

    # Validate email format
    while '@' not in admin_email or '.' not in admin_email.split('@')[1]:
        print_error("Invalid email format")
        admin_email = ask_text("Google Workspace admin email")

    console.print()

    # Step 3: Validate Credentials
    print_section("✓ Validating Credentials")

    with create_spinner() as progress:
        task = progress.add_task("Checking service account and credentials...", total=None)

        is_valid, domain, error = validate_credentials(service_account_path, admin_email)

    console.print()

    if not is_valid:
        print_error(f"Credential validation failed: {error}")
        console.print()
        console.print("[yellow]Common issues:[/yellow]")
        console.print("  • Ensure domain-wide delegation is enabled in Google Cloud Console")
        console.print("  • Verify the OAuth scopes are authorized in Workspace Admin Console")
        console.print("  • Confirm the admin email is correct\n")
        console.print("[cyan]For help, see the setup guide or try again with:[/cyan]")
        console.print("[bold]  hancock init[/bold]\n")
        return

    print_success(f"Credentials validated successfully!")
    if domain:
        print_info(f"Domain: {domain}")
    console.print()

    # Step 4: Save Configuration
    print_section("💾 Saving Configuration")

    config_data = {
        'service_account_file': str(service_account_path),
        'admin_email': admin_email,
    }

    config.save(config_data)

    print_success(f"Configuration saved to {config.get_config_path()}")
    console.print()

    # Success!
    console.print("[bold green]🎉 You're all set![/bold green]\n")

    console.print("[cyan]Your credentials will stay exactly where you keep them.\nWe just remember the path so we can find them when needed.[/cyan]\n")

    console.print("[bold]Next steps:[/bold]")
    console.print("  1. Create a folder with your signature HTML files")
    console.print("  2. Name each file to match a user (e.g., [cyan]john.smith.html[/cyan])")
    console.print("  3. Run: [bold green]hancock deploy signatures/[/bold green]\n")

    console.print("[muted]Need help creating signatures? Try:[/muted]")
    console.print("[muted]  hancock --help[/muted]\n")
