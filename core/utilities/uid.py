import uuid

from django.utils import timezone


def generate_uid(prefix: str) -> str:
    """
    Utility for generating a unique ID to be used
    on certain model fields.

    Args:
        prefix (str): The prefix for the customized unique id.

    Returns:
        str: The generated unique id string.
    """
    # Get the current date in MMDDYY formatting. (e.g. 092524)
    today = timezone.now().strftime('%m%d%y')

    # Random UUID, gets the last 6 characters.
    uuid_str = uuid.uuid4().hex[:6].upper()

    # Return the generated unique id string.
    return f'{prefix}-{today}-{uuid_str}'
