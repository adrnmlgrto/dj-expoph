from loguru import logger
from ninja import File, Form, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile

from core.schemas.error import Http422Message, Http500Message

from ..models import CustomUser
from ..resources.register import register_user as reg_user
from .schemas import UserSchemaIn, UserSchemaOut

# Define the users API route.
router = Router(tags=['users'])


@router.post(
    '/',
    response={
        201: UserSchemaOut,
        422: Http422Message,
        500: Http500Message
    }
)
def register_user(
    request,
    details: Form[UserSchemaIn],
    avatar: UploadedFile | None = File(None)
):
    """
    Register a user into the system.
    """
    try:

        # NOTE: Do NOT log the payload data that uses
        # `model_dump()` with secrets. (See `ClientSchemaIn`)

        # Create the client record using the details.
        client: CustomUser = reg_user(
            avatar=avatar, **details.model_dump()
        )

        return 201, client

    except Exception as e:
        logger.exception(e)
        raise HttpError(
            500,
            ('Something went wrong while processing your request. '
             'Please contact the system administrator.')
        )
