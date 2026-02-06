"""Gmail API integration for deploying signatures."""

from typing import Dict, List, Tuple, Optional, Callable
from googleapiclient.errors import HttpError
import time


def deploy_signature(service, user_email: str, signature_html: str) -> Tuple[bool, Optional[str]]:
    """
    Deploy signature to a single user's Gmail account.

    Args:
        service: Authenticated Gmail API service
        user_email: User's email address
        signature_html: HTML signature content

    Returns:
        Tuple of (success: bool, error_message: Optional[str])
    """
    try:
        # Get the user's sendAs settings
        send_as_list = service.users().settings().sendAs().list(userId=user_email).execute()

        if not send_as_list.get('sendAs'):
            return False, "No sendAs configuration found"

        # Update the primary sendAs (usually the first one)
        primary_send_as = send_as_list['sendAs'][0]
        send_as_email = primary_send_as.get('sendAsEmail', user_email)

        # Update the signature
        service.users().settings().sendAs().patch(
            userId=user_email,
            sendAsEmail=send_as_email,
            body={'signature': signature_html}
        ).execute()

        return True, None

    except HttpError as error:
        error_msg = f"HTTP {error.resp.status}: {error.content.decode('utf-8')}"
        return False, error_msg
    except Exception as e:
        return False, str(e)


def get_current_signature(service, user_email: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Get the current signature for a user.

    Args:
        service: Authenticated Gmail API service
        user_email: User's email address

    Returns:
        Tuple of (success: bool, signature_html: Optional[str], error_message: Optional[str])
    """
    try:
        # Get the user's sendAs settings
        send_as_list = service.users().settings().sendAs().list(userId=user_email).execute()

        if not send_as_list.get('sendAs'):
            return False, None, "No sendAs configuration found"

        # Get the primary sendAs (usually the first one)
        primary_send_as = send_as_list['sendAs'][0]
        signature = primary_send_as.get('signature', '')

        return True, signature, None

    except HttpError as error:
        error_msg = f"HTTP {error.resp.status}: {error.content.decode('utf-8')}"
        return False, None, error_msg
    except Exception as e:
        return False, None, str(e)


def deploy_signatures_batch(
    service,
    signatures: Dict[str, str],
    retry_attempts: int = 3,
    retry_delay: int = 2,
    progress_callback: Optional[Callable[[str, bool, Optional[str]], None]] = None
) -> Tuple[int, int, List[Dict]]:
    """
    Deploy signatures to multiple users with retry logic.

    Args:
        service: Authenticated Gmail API service
        signatures: Dictionary mapping email -> signature HTML
        retry_attempts: Number of retry attempts on failure
        retry_delay: Delay between retries (seconds)
        progress_callback: Optional callback function(email, success, error_msg)

    Returns:
        Tuple of (success_count, failed_count, errors_list)
    """
    success_count = 0
    failed_count = 0
    errors = []

    for user_email, signature_html in signatures.items():
        # Retry logic
        success = False
        error_msg = None

        for attempt in range(retry_attempts):
            success, error_msg = deploy_signature(service, user_email, signature_html)
            if success:
                break
            if attempt < retry_attempts - 1:
                time.sleep(retry_delay)

        if success:
            success_count += 1
        else:
            failed_count += 1
            errors.append({
                'email': user_email,
                'error': error_msg
            })

        # Call progress callback if provided
        if progress_callback:
            progress_callback(user_email, success, error_msg)

        # Small delay for rate limiting
        time.sleep(0.1)

    return success_count, failed_count, errors
