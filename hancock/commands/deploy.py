"""Deploy signatures to Google Workspace users."""

from pathlib import Path
from ..core.config import get_config
from ..core.auth import authenticate, get_service
from ..core.directory import get_all_users, extract_user_data
from ..core.matching import match_signatures_to_users
from ..core.gmail import deploy_signatures_batch
from ..ui import (
    console,
    print_header,
    print_success,
    print_error,
    print_warning,
    print_section,
    ask_yes_no,
    create_match_table,
    print_summary,
    print_deployment_summary,
    create_progress_bar,
    create_spinner,
)


def run_deploy(folder_path: str, dry_run: bool = False):
    """
    Deploy signatures from a folder to Google Workspace users.

    Args:
        folder_path: Path to folder containing signature HTML files
        dry_run: If True, only show what would be deployed without actually deploying
    """
    print_header("🚀 Hancock Signature Deployment")

    # Check configuration
    config = get_config()
    if not config.is_configured():
        print_error("Hancock is not configured yet")
        console.print("\n[cyan]Run this command first:[/cyan]")
        console.print("[bold]  hancock init[/bold]\n")
        return

    # Validate folder path
    signatures_folder = Path(folder_path).expanduser().absolute()
    if not signatures_folder.exists():
        print_error(f"Folder not found: {signatures_folder}")
        return

    if not signatures_folder.is_dir():
        print_error(f"Path is not a directory: {signatures_folder}")
        return

    console.print(f"[cyan]📁 Signatures folder: {signatures_folder}[/cyan]\n")

    # Authenticate
    print_section("🔐 Authenticating with Google Workspace")

    try:
        with create_spinner() as progress:
            task = progress.add_task("Connecting to Google Workspace...", total=None)

            credentials, _ = authenticate(
                config.get('service_account_file'),
                config.get('admin_email')
            )

            directory_service = get_service('admin', 'directory_v1', credentials)
            gmail_service = get_service('gmail', 'v1', credentials)

        print_success("Connected to Google Workspace")
        console.print()

    except Exception as e:
        print_error(f"Authentication failed: {e}")
        console.print("\n[yellow]Try running:[/yellow] [bold]hancock init[/bold]\n")
        return

    # Fetch users
    print_section("👥 Fetching Users")

    try:
        with create_spinner() as progress:
            task = progress.add_task("Loading users from your workspace...", total=None)
            users_raw = get_all_users(directory_service)

        users = [extract_user_data(u) for u in users_raw]
        print_success(f"Found {len(users)} users in your workspace")
        console.print()

    except Exception as e:
        print_error(f"Failed to fetch users: {e}")
        return

    # Match signatures to users
    print_section("🔍 Matching Signatures")

    try:
        matched, unmatched, errors = match_signatures_to_users(signatures_folder, users)

        console.print(f"[cyan]Found {len(matched) + len(unmatched) + len(errors)} HTML files[/cyan]\n")

        # Display match table
        table = create_match_table(matched, unmatched, errors)
        console.print(table)

        # Summary
        print_summary(len(matched), len(unmatched), len(errors))

    except ValueError as e:
        print_error(str(e))
        return
    except Exception as e:
        print_error(f"Error matching signatures: {e}")
        return

    # Check if there are any signatures to deploy
    if not matched:
        print_warning("No signatures matched to users")
        console.print("\n[yellow]Make sure your filenames match user emails or names.[/yellow]")
        console.print("[yellow]Example: john.smith.html → john.smith@yourcompany.com[/yellow]\n")
        return

    # Show warnings for external images
    external_image_warnings = []
    for match in matched:
        if match.get('info', {}).get('has_external_images'):
            external_image_warnings.append(match['email'])

    if external_image_warnings:
        console.print("[yellow]⚠ Warning: Some signatures contain external images[/yellow]")
        console.print("[muted]External images require hosting and may not display correctly in all email clients.[/muted]")
        console.print("[muted]Consider using base64-encoded images instead.[/muted]\n")

    # Dry run mode
    if dry_run:
        console.print("[bold yellow]🔍 DRY RUN MODE - No signatures will be deployed[/bold yellow]\n")
        console.print("[cyan]The above signatures would be deployed to Google Workspace.[/cyan]")
        console.print("[cyan]Remove --dry-run to actually deploy.[/cyan]\n")
        return

    # Confirm deployment
    console.print(f"[bold]Ready to deploy {len(matched)} signatures to Google Workspace?[/bold]\n")
    console.print("[muted]This will update Gmail signatures for the matched users.[/muted]\n")

    if not ask_yes_no("Deploy signatures?", default=False):
        console.print("\n[yellow]Deployment cancelled[/yellow]\n")
        return

    console.print()

    # Deploy signatures
    print_section("📤 Deploying Signatures")

    # Prepare signatures dict
    signatures_dict = {}
    for match in matched:
        with open(match['path'], 'r', encoding='utf-8') as f:
            signatures_dict[match['email']] = f.read()

    # Deploy with progress bar
    success_count = 0
    failed_count = 0
    errors_list = []

    with create_progress_bar() as progress:
        task = progress.add_task("Deploying signatures...", total=len(matched))

        def progress_callback(email, success, error_msg):
            nonlocal success_count, failed_count
            if success:
                success_count += 1
            else:
                failed_count += 1
                errors_list.append({'email': email, 'error': error_msg})
            progress.update(task, advance=1)

        success_count, failed_count, errors_list = deploy_signatures_batch(
            gmail_service,
            signatures_dict,
            progress_callback=progress_callback
        )

    console.print()

    # Show results
    print_deployment_summary(success_count, failed_count, len(unmatched))

    if errors_list:
        console.print("[bold red]Errors:[/bold red]")
        for error in errors_list[:5]:  # Show first 5
            console.print(f"  [red]• {error['email']}: {error['error']}[/red]")
        if len(errors_list) > 5:
            console.print(f"  [muted]... and {len(errors_list) - 5} more errors[/muted]")
        console.print()

    if success_count > 0:
        console.print("[bold green]Done! 🎉[/bold green]\n")
