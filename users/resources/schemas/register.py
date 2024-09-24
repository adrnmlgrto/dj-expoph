from pydantic import BaseModel, EmailStr, Field, field_serializer
from pydantic.types import SecretStr
from ninja.files import UploadedFile

from users.models.utils import Department

__all__ = [
    'RegisterAdmin',
    'RegisterClient'
]


class RegisterBase(BaseModel):
    """
    Base user fields for validation using `pydantic.BaseModel`.
    """
    username: str = Field(
        ...,
        description='Client username for authentication.'
    )
    email: EmailStr = Field(
        ...,
        description='Client email for authentication.'
    )
    password: SecretStr = Field(
        ...,
        description='Client password for authentication.'
    )

    @field_serializer('password')
    def serialize_password_str(self, v: SecretStr):
        """
        Retrieve the actual password's value upon serialization.
        """
        return v.get_secret_value()


class RegisterAdmin(RegisterBase):
    """
    Basemodel for validating client registration parameters.
    """
    first_name: str = Field(
        ...,
        description='Admin user\'s first name.'
    )
    last_name: str | None = Field(
        ...,
        description='Admin user\'s last name.'
    )
    department: Department = Field(
        default=Department.ADMIN,
        description='Admin user\'s designated department or role.'
    )
    avatar: UploadedFile | None = Field(
        default=None,
        description='Avatar file for the admin user.'
    )


class RegisterClient(RegisterBase):
    """
    Basemodel for validating client registration parameters.
    """
    mobile_number: str = Field(
        ...,
        description='Mobile number of the client user.'
    )
    display_name: str | None = Field(
        None,
        description='Name to display for the client user.'
    )
    # TODO: Change shipping address into parts.
    # (e.g. House No., Street, City, Country etc.)
    shipping_address: str | None = Field(
        None,
        description='Shipping address of the client user.'
    )
    avatar: UploadedFile | None = Field(
        None,
        description='Avatar file for the client user.'
    )
