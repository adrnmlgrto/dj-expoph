from datetime import datetime

from ninja import Field, Schema
from pydantic import EmailStr, field_serializer
from pydantic.types import SecretStr

from ..models.utils import UserStatus


class UserSchemaIn(Schema):
    """
    Schema for validating user request payload data.
    """
    email: EmailStr = Field(
        ...,
        description='Email to set for the user.'
    )
    password: SecretStr = Field(
        ...,
        description='Password to set for the user.'
    )
    display_name: str = Field(
        None,
        description='Name to display for the user.'
    )

    @field_serializer('password')
    def serialize_password_str(self, pw: SecretStr):
        return pw.get_secret_value()


class UserSchemaOut(Schema):
    """
    Schema for defining the response data for user representation.
    """
    email: EmailStr = Field(
        ...,
        description='User\'s email for authentication.',
        examples=['johndoe@expoph.com']
    )
    display_name: str = Field(
        ...,
        description='Name to display for the client user.',
        examples=['johndoe01']
    )
    status: UserStatus = Field(
        ...,
        description='Client user\'s current status.',
        examples=UserStatus.values
    )
    created_at: datetime = Field(
        ...,
        description='Time of creation for the user.'
    )
    modified_at: datetime = Field(
        ...,
        description='Time of modification for the user.'
    )

    @field_serializer('status')
    def serialize_status_label(self, v: UserStatus):
        return v.label
