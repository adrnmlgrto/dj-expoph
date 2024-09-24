from loguru import logger
from ninja import File, Form, Path, Router
from ninja.errors import HttpError
from ninja.files import UploadedFile

from core.schemas.error import Http404Message, Http500Message

from ..models import Client
from ..resources.register import register_client as register_client_user
from .schemas import ClientSchemaIn, ClientSchemaOut, GetClientPath

router = Router(tags=['clients'])


@router.post(
    '/register',
    response={
        201: ClientSchemaOut,
        500: Http500Message
    }
)
def register_client(
    request,
    details: Form[ClientSchemaIn],
    avatar: UploadedFile | None = File(None)
):
    """
    Register a client user to the system.
    """
    try:

        # Create the client record using the details.
        client: Client = register_client_user(
            avatar=avatar, **details.model_dump()
        )

        # NOTE: Do NOT log the payload data that uses
        # `model_dump()` with secrets. (See `ClientSchemaIn`)

        return 201, client

    except Exception as e:
        logger.exception(e)
        raise HttpError(
            500,
            ('Something went wrong while processing your request. '
             'Please contact the system administrator.')
        )


@router.get(
    '/{username}',
    response={
        200: ClientSchemaOut,
        404: Http404Message,
        500: Http500Message
    }
)
def get_client(request, user: Path[GetClientPath]):
    """
    Retrieve client user details.
    """
    try:

        # Query the client table based on username.
        client = Client.objects.get(user__username=user.username)

        # Return the client response.
        return 200, client

    except Client.DoesNotExist:
        logger.error(f'Client {user.username} was not found.')
        raise HttpError(404, 'Client user does not exist.')
