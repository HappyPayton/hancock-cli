"""Google Directory API integration for fetching users."""

from typing import List, Dict, Optional
from googleapiclient.errors import HttpError


def get_all_users(service, max_results: int = 500) -> List[Dict]:
    """
    Fetch all users from Google Workspace Directory.

    Args:
        service: Authenticated Directory API service
        max_results: Maximum results per page (max 500)

    Returns:
        List of user dictionaries with user data
    """
    users = []
    page_token = None

    try:
        while True:
            request = service.users().list(
                customer='my_customer',  # Get all users in admin's domain
                maxResults=min(max_results, 500),
                pageToken=page_token,
                orderBy='email',
                projection='full'  # Get full user data
            )

            response = request.execute()

            if 'users' in response:
                users.extend(response['users'])

            page_token = response.get('nextPageToken')
            if not page_token:
                break

    except HttpError as error:
        raise Exception(f"Error fetching users: {error}")

    return users


def extract_user_data(user: Dict) -> Dict:
    """
    Extract and normalize user data.

    Args:
        user: User dictionary from Directory API

    Returns:
        Dictionary with normalized user data
    """
    name = user.get('name', {})

    # Get primary email
    primary_email = user.get('primaryEmail', '')

    return {
        'email': primary_email,
        'name': name.get('fullName') or f"{name.get('givenName', '')} {name.get('familyName', '')}".strip(),
        'first_name': name.get('givenName', ''),
        'last_name': name.get('familyName', ''),
    }
