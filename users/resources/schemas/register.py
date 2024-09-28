from ninja.files import UploadedFile
from pydantic import BaseModel, EmailStr, Field, field_serializer
from pydantic.types import SecretStr

__all__ = [
    'RegisterUser',
    'RegisterStaffUser'
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


class RegisterUser(BaseModel):
    """
    Basemodel for validating user registration parameters.
    """
    email: EmailStr = Field(
        ...,
        description='Client email for authentication.'
    )
    password: SecretStr = Field(
        ...,
        description='Client password for authentication.'
    )
    avatar: UploadedFile | None = Field(
        None,
        description='Avatar file for the client user.'
    )
    display_name: str | None = Field(
        None,
        description='Name to display for the client user.'
    )

    @field_serializer('password')
    def serialize_password_str(self, v: SecretStr):
        """
        Retrieve the actual password's value upon serialization.
        """
        return v.get_secret_value()


class RegisterStaffUser(RegisterUser):
    """
    Basemodel for validating staff user registration parameters.
    NOTE: Override field(s) from inherited basemodel if needed for staff user.
    """
    pass
