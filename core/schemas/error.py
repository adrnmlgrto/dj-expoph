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


class Http422Message(Schema):
    detail: list[dict[str, str]] = Field(
        ...,
        examples=[
            [
                {
                    'type': 'missing',
                    'loc': ['field1', 'field2'],
                    'msg': 'Field required'
                }
            ]
        ]
    )


class Http500Message(Schema):
    detail: str = Field(
        ...,
        examples=[
            ('Something went wrong while processing your request. '
             'Please contact the system administrator.')
        ]
    )
