"""Google Workspace authentication module."""

import os
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from typing import Tuple, Optional

# Required scopes for Hancock
SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user.readonly',
    'https://www.googleapis.com/auth/gmail.settings.basic'
]


def authenticate(service_account_file: str, admin_email: str) -> Tuple[object, None]:
    """
    Authenticate with Google Workspace using Service Account with Domain-Wide Delegation.

    Args:
        service_account_file: Path to service account JSON key file
        admin_email: Admin email for domain-wide delegation

    Returns:
        Tuple of (credentials, None) for service account auth

    Raises:
        FileNotFoundError: If service account file doesn't exist
        ValueError: If credentials are invalid
    """
    service_account_path = Path(service_account_file).expanduser()

    if not service_account_path.exists():
        raise FileNotFoundError(
            f"Service account file not found: {service_account_path}\n"
            "Please ensure the path is correct."
        )

    try:
        credentials = service_account.Credentials.from_service_account_file(
            str(service_account_path),
            scopes=SCOPES
        )

        # Create delegated credentials for domain-wide access
        delegated_credentials = credentials.with_subject(admin_email)

        return delegated_credentials, None
    except Exception as e:
        raise ValueError(f"Failed to load credentials: {str(e)}")


def get_service(api_name: str, api_version: str, credentials) -> object:
    """
    Build and return a Google API service client.

    Args:
        api_name: Name of the API (e.g., 'admin', 'gmail')
        api_version: API version (e.g., 'directory_v1', 'v1')
        credentials: Authenticated credentials

    Returns:
        API service client
    """
    return build(api_name, api_version, credentials=credentials, cache_discovery=False)


def validate_credentials(service_account_file: str, admin_email: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Validate service account credentials and extract domain.

    Args:
        service_account_file: Path to service account JSON key file
        admin_email: Admin email for domain-wide delegation

    Returns:
        Tuple of (is_valid, domain, error_message)
    """
    try:
        credentials, _ = authenticate(service_account_file, admin_email)

        # Try to make a simple API call to verify credentials work
        service = get_service('admin', 'directory_v1', credentials)

        # Extract domain from admin email
        domain = admin_email.split('@')[1] if '@' in admin_email else None

        # Verify we can access the directory (minimal call)
        try:
            service.users().list(domain=domain, maxResults=1).execute()
            return True, domain, None
        except Exception as e:
            return False, domain, f"API access failed: {str(e)}"

    except FileNotFoundError as e:
        return False, None, str(e)
    except ValueError as e:
        return False, None, str(e)
    except Exception as e:
        return False, None, f"Unexpected error: {str(e)}"
