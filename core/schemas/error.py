from ninja import Schema, Field


class Http403Message(Schema):
    detail: str = Field(
        ...,
        examples=[
            ('You don\'t have permission to access '
             'this resource on this server.')
        ]
    )


class Http404Message(Schema):
    detail: str = Field(
        ...,
        examples=['Resource does not exist.']
    )


class Http500Message(Schema):
    detail: str = Field(
        ...,
        examples=[
            ('Something went wrong while processing your request. '
             'Please contact the system administrator.')
        ]
    )
