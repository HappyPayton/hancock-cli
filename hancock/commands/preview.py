"""Preview current signature for a user."""

from ..core.config import get_config
from ..core.auth import authenticate, get_service
from ..core.gmail import get_current_signature
from ..ui import (
    console,
    print_header,
    print_success,
    print_error,
    print_section,
    create_spinner,
)


def run_preview(email: str):
    """
    Preview the current signature for a user.

    Args:
        email: User's email address
    """
    print_header(f"📧 Preview Signature for {email}")

    # Check configuration
    config = get_config()
    if not config.is_configured():
        print_error("Hancock is not configured yet")
        console.print("\n[cyan]Run this command first:[/cyan]")
        console.print("[bold]  hancock init[/bold]\n")
        return

    # Authenticate
    try:
        with create_spinner() as progress:
            task = progress.add_task("Connecting to Google Workspace...", total=None)

            credentials, _ = authenticate(
                config.get('service_account_file'),
                config.get('admin_email')
            )

            gmail_service = get_service('gmail', 'v1', credentials)

        console.print()

    except Exception as e:
        print_error(f"Authentication failed: {e}")
        return

    # Get current signature
    print_section("🔍 Fetching Current Signature")

    try:
        success, signature_html, error = get_current_signature(gmail_service, email)

        if not success:
            print_error(f"Failed to get signature: {error}")
            return

        if not signature_html:
            console.print(f"[yellow]No signature set for {email}[/yellow]\n")
            return

        print_success(f"Current signature for {email}:")
        console.print()

        # Display signature HTML
        console.print("[cyan]═══ Signature HTML ═══[/cyan]")
        console.print(signature_html)
        console.print("[cyan]═══ End of Signature ═══[/cyan]\n")

        # Show size
        size_bytes = len(signature_html.encode('utf-8'))
        size_kb = size_bytes / 1024
        console.print(f"[muted]Size: {size_kb:.1f}KB ({size_bytes} bytes)[/muted]\n")

    except Exception as e:
        print_error(f"Error: {e}")
