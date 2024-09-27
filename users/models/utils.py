from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

from core.utilities.uid import generate_uid


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
    ACTIVE = 'A', _('Active')
    SUSPENDED = 'S', _('Suspended')
    PENDING = 'P', _('Pending Verification')
    UNKNOWN = 'U', _('Unknown')


def generate_admin_number(department: Department | str) -> str:
    """
    Generates a unique admin number based on the department prefix.

    Format: <DEPT-PREFIX>-<MMDDYY>-<6-CHAR-UUID>
    Example: SYS-092524-9F1A73
    """
    # Define department prefixes.
    DEPARTMENT_PREFIX_MAP = {
        Department.ADMIN: 'SYS',
        Department.BILLING: 'BIL',
        Department.SALES: 'SAL',
        Department.MARKETING: 'MKT',
        Department.SUPPORT: 'SUP'
    }

    # Get the prefix based on the department.
    prefix = DEPARTMENT_PREFIX_MAP.get(department)

    # In case prefix is `None`, we'll raise an error.
    if not prefix:
        raise ValueError(_(f'Department "{department}" is invalid.'))

    # Return the generated admin number w/ prefix.
    return generate_uid(prefix)


def generate_client_number() -> str:
    """
    Generates a unique admin number based on the department prefix.

    Format: <CX>-<MMDDYY>-<6-CHAR-UUID>
    Example: CX-092524-9F1A73
    """
    # Define client prefix.
    CLIENT_PREFIX = 'CX'

    # Return the generated client number w/ prefix.
    return generate_uid(CLIENT_PREFIX)
