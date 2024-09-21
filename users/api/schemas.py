from datetime import datetime

from ninja import Field, Schema
from pydantic import SecretStr, field_serializer

from ..models.utils import UserStatus


class GetClientPath(Schema):
    username: str = Field(
        ...,
        description='Client\'s username to retrieve.'
    )


class ClientSchemaIn(Schema):
    username: str = Field(
        ...,
        description='Client\'s username for authentication.'
    )
    email: str = Field(
        ...,
        description='Email to set for the client user.'
    )
    password: SecretStr = Field(
        ...,
        description='Password to set for the client user.'
    )
    mobile_number: str = Field(
        ...,
        description='Mobile number of the client user.'
    )
    display_name: str | None = Field(
        None,
        description='Name to display for the client user.'
    )
    shipping_address: str | None = Field(
        None,
        description='Shipping address of the client user.'
    )

    @field_serializer('password')
    def serialize_password_str(self, v: SecretStr):
        return v.get_secret_value()


class UserSchemaOut(Schema):
    username: str
    email: str


class ClientSchemaOut(Schema):
    user: UserSchemaOut
    mobile_number: str = Field(
        ...,
        description='Mobile number of the client user.',
        examples=['+639123456789']
    )
    avatar: str | None = Field(
        None,
        description='Avatar image of the client user.',
        examples=['/media/clients/johndoe01/uploads/avatar/IMG_001.jpg']
    )
    display_name: str | None = Field(
        None,
        description='Name to display for the client user.',
        examples=['johndoe01']
    )
    shipping_address: str | None = Field(
        None,
        description='Shipping address of the client user.',
        examples=['123 Main St., Quezon City, 1112']
    )
    status: UserStatus = Field(
        ...,
        description='Client user\'s current status.',
        examples=['A', 'P', 'S', 'U']
    )
    created_at: datetime
    modified_at: datetime
