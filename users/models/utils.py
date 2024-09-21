import uuid

from django.db.models import TextChoices

__all__ = [
    'Department',
    'UserStatus',
    'generate_admin_number'
]


class Department(TextChoices):
    """
    Status choice(s) for departments for admin users.
    """
    ADMIN = 'sysadmin', 'System Administrator'
    BILLING = 'billing', 'Billing Administrator'
    PRODUCT_MANAGER = 'product_manager', 'Product Manager'
    SALES = 'sales', 'Sales'
    MARKETING = 'marketing', 'Marketing'
    SUPPORT = 'support', 'Customer Support'


class UserStatus(TextChoices):
    """
    Status choice(s) for users (client / admin).
    """
    ACTIVE = 'A', 'Active'
    SUSPENDED = 'S', 'Suspended'
    PENDING = 'P', 'Pending Verification'
    UNKNOWN = 'U', 'Unknown Status'


def generate_admin_number(department: Department | str) -> str:
    """
    Generates a unique admin number based on the department prefix.

    Format: <DEPT-PREFIX>-<SHORT-UUID>
    Example: SYS-9F1A73B4
    """
    # Define department prefixes.
    department_prefix_map = {
        Department.ADMIN: 'SYS',
        Department.BILLING: 'BIL',
        Department.SALES: 'SAL',
        Department.MARKETING: 'MKT',
        Department.SUPPORT: 'SUP'
    }

    # Get the prefix based on the department.
    prefix = department_prefix_map.get(department)

    # In case prefix is `None`, we'll raise an error.
    if not prefix:
        raise ValueError(f'Department "{department}" is invalid.')

    # Generate a short UUID and capitalize all characters.
    short_uuid = str(uuid.uuid4())[:8].upper()

    return f'{prefix}-{short_uuid}'
