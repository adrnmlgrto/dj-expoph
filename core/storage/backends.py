import os
from typing import override

from loguru import logger
from storages.backends.s3 import S3Storage
from storages.utils import clean_name
from supabase import Client, create_client

from .exceptions import SupabaseObjectError


class SupabaseS3Storage(S3Storage):
    """
    Overridden storage class for S3-compatible buckets on Supabase.
    """

    @override
    def url(self, name, parameters=None, expire=None, http_method=None):
        """
        Generates a signed URL for accessing a file in the
        Supabase storage bucket.

        Args:
            name (str): The name of the file to generate a signed URL for.
            parameters (dict, optional): Additional parameters to include in
                the signed URL. Defaults to None.
            expire (int, optional): The time in seconds until the signed URL
                expires. Defaults to None.
            http_method (str, optional): The HTTP method to use when accessing
                the file. Defaults to None.

        Returns:
            str: The signed URL for accessing the file. Will return the
                default S3 URL if an error occurs.
        """
        try:
            # Normalize and clean the name of the file from params.
            name = self._normalize_name(clean_name(name))

            # Initialize the `supabase` client.
            sb: Client = create_client(
                supabase_url=os.getenv('SUPABASE_API_URL'),
                supabase_key=os.getenv('SUPABASE_API_KEY'),
            )
            # Make an API request to get the "signedURL" from the response.
            response = sb.storage.from_('expoph-bucket').create_signed_url(
                path=name,
                expires_in=self.querystring_expire,  # 3600s
            )
            url = response.get('signedURL', None)

            # Raise error when response doesn't contain the signed url.
            if url is None:
                raise SupabaseObjectError(
                    'Signed URL from supabase is empty or none.'
                )
            return response.get("signedURL")

        except Exception as e:
            # Call the original `S3Storage.url()` as fallback.
            logger.error(f'Error retrieving supabase-signed url: {e}')
            return super().url(name, parameters, expire, http_method)
