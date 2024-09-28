import os
from typing import override

from loguru import logger
from storages.backends.s3 import S3Storage
from supabase import Client, create_client


class SupabaseObjectError(Exception):
    pass


class SupabaseS3Storage(S3Storage):
    """
    Overridden storage class for S3-compatible buckets on Supabase.
    """
    @override
    def url(self, *args, **kwargs):

        try:

            # Initialize the `supabase` client.
            sb: Client = create_client(
                supabase_url=os.getenv('SUPABASE_API_URL'),
                supabase_key=os.getenv('SUPABASE_API_KEY')
            )
            # Retrieve the "signedURL" from the response.
            response = sb.storage.from_('expoph-bucket').create_signed_url(
                path='users/Sakuuu/avatar.png',
                expires_in=self.querystring_expire  # 3600s from S3Storage
            )
            url = response.get('signedURL', None)

            if url is None:
                raise SupabaseObjectError(
                    'Signed URL from supabase is empty or none.'
                )
            return response.get('signedURL')

        except Exception as e:

            # Log only that an exception occurred.
            logger.error(
                f'Error retrieving supabase-signed url: {e}'
            )
            # Call the original `S3Storage.url()` as fallback.
            return super().url(*args, **kwargs)
