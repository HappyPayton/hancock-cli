"""Signature file to user matching logic."""

import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Gmail signature size limit (approximately 10KB)
MAX_SIGNATURE_SIZE = 10 * 1024  # 10KB in bytes


def normalize_name(name: str) -> str:
    """
    Normalize a name for matching purposes.
    - Remove 'sig' suffix
    - Convert to lowercase
    - Remove special characters
    - Replace separators with spaces

    Args:
        name: Filename or email prefix to normalize

    Returns:
        Normalized string for matching
    """
    # Remove file extension
    name = Path(name).stem

    # Remove 'sig' or 'signature' suffix (case insensitive)
    name = re.sub(r'(sig|signature)$', '', name, flags=re.IGNORECASE)

    # Convert to lowercase
    name = name.lower()

    # Replace common separators with spaces
    name = re.sub(r'[._-]', ' ', name)

    # Remove any remaining special characters
    name = re.sub(r'[^a-z0-9\s]', '', name)

    # Normalize whitespace
    name = ' '.join(name.split())

    return name


def match_filename_to_user(filename: str, user_data: Dict) -> bool:
    """
    Check if a filename matches a user's data.

    Tries multiple matching strategies:
    1. Email prefix (before @)
    2. Full name
    3. First + last name combinations

    Args:
        filename: Signature filename (with or without extension)
        user_data: User data dictionary with email, name, first_name, last_name

    Returns:
        True if filename matches user, False otherwise
    """
    normalized_filename = normalize_name(filename)

    # Strategy 1: Match email prefix
    email = user_data.get('email', '')
    if email:
        email_prefix = email.split('@')[0].lower()
        normalized_email = normalize_name(email_prefix)
        if normalized_filename == normalized_email:
            return True

    # Strategy 2: Match full name
    full_name = user_data.get('name', '')
    if full_name:
        normalized_name_val = normalize_name(full_name)
        if normalized_filename == normalized_name_val:
            return True

    # Strategy 3: Match first + last name
    first_name = user_data.get('first_name', '').lower()
    last_name = user_data.get('last_name', '').lower()

    if first_name and last_name:
        # Try various combinations
        combinations = [
            f"{first_name} {last_name}",
            f"{first_name}{last_name}",
            f"{last_name} {first_name}",
            f"{last_name}{first_name}",
        ]

        for combo in combinations:
            normalized_combo = normalize_name(combo)
            if normalized_filename == normalized_combo:
                return True

    return False


def validate_signature_file(file_path: Path) -> Tuple[bool, Optional[str], Dict]:
    """
    Validate a signature HTML file.

    Checks:
    - File exists and is readable
    - File size is within limits
    - Contains HTML content
    - Analyzes image usage (base64 vs external URLs)

    Args:
        file_path: Path to signature HTML file

    Returns:
        Tuple of (is_valid, error_message, info_dict)
    """
    info = {
        'size': 0,
        'has_base64_images': False,
        'has_external_images': False,
        'external_image_urls': [],
    }

    # Check file exists
    if not file_path.exists():
        return False, f"File not found: {file_path}", info

    # Check file is readable
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, f"Could not read file: {e}", info

    # Check file size
    file_size = len(content.encode('utf-8'))
    info['size'] = file_size

    if file_size > MAX_SIGNATURE_SIZE:
        return False, f"File size ({file_size} bytes) exceeds limit ({MAX_SIGNATURE_SIZE} bytes)", info

    # Basic HTML validation
    if not content.strip():
        return False, "File is empty", info

    # Analyze images
    # Check for base64 encoded images
    if 'data:image' in content:
        info['has_base64_images'] = True

    # Check for external image URLs (img src with http/https)
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    img_matches = re.findall(img_pattern, content, re.IGNORECASE)

    for img_src in img_matches:
        if img_src.startswith(('http://', 'https://', '//')):
            info['has_external_images'] = True
            info['external_image_urls'].append(img_src)

    return True, None, info


def match_signatures_to_users(
    signatures_folder: Path,
    users: List[Dict]
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Match signature HTML files to users.

    Args:
        signatures_folder: Path to folder containing signature HTML files
        users: List of user dictionaries from Directory API

    Returns:
        Tuple of (matched, unmatched, errors)
        - matched: List of dicts with {filename, email, name, path, size, info}
        - unmatched: List of dicts with {filename, path}
        - errors: List of dicts with {filename, path, error}
    """
    if not signatures_folder.exists():
        raise FileNotFoundError(f"Signatures folder not found: {signatures_folder}")

    if not signatures_folder.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {signatures_folder}")

    # Get all HTML files
    html_files = list(signatures_folder.glob('*.html')) + list(signatures_folder.glob('*.htm'))

    if not html_files:
        raise ValueError(f"No HTML files found in {signatures_folder}")

    matched = []
    errors = []
    matched_files = set()

    # Match files to users
    for user_data in users:
        user_email = user_data.get('email')
        if not user_email:
            continue

        # Try to find a matching file
        matched_file = None
        for file_path in html_files:
            if match_filename_to_user(file_path.name, user_data):
                matched_file = file_path
                break

        if matched_file:
            # Validate the file
            is_valid, error_msg, info = validate_signature_file(matched_file)

            if not is_valid:
                errors.append({
                    'filename': matched_file.name,
                    'path': str(matched_file),
                    'error': error_msg
                })
                continue

            # Add to matched list
            matched.append({
                'filename': matched_file.name,
                'email': user_email,
                'name': user_data.get('name', ''),
                'path': str(matched_file),
                'size': info['size'],
                'info': info
            })
            matched_files.add(matched_file)

    # Find unmatched files
    unmatched = []
    for file_path in html_files:
        if file_path not in matched_files:
            unmatched.append({
                'filename': file_path.name,
                'path': str(file_path)
            })

    return matched, unmatched, errors
