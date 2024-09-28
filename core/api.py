from django.contrib.admin.views.decorators import staff_member_required
from ninja import NinjaAPI, Redoc

# Instantiate the NinjaAPI object.
api = NinjaAPI(
    docs=Redoc(),
    docs_decorator=staff_member_required,
    title='Expo PH API',
    description=(
        'This is the official API for Expo PH for the '
        'individual resource endpoints.'
    ),
    version='1.0.1'
)


# TODO: Add routers per application. (09-19-2024)
api.add_router('/users/', 'users.api.user.router')
