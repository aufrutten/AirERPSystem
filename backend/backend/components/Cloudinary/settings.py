import cloudinary
from decouple import config
from django.conf import settings

# Default: DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
if not settings.DEBUG:  # pragma: no cover
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    # Cloudinary
    cloudinary.config(
        cloud_name=config('CLOUD_NAME', cast=str),
        api_key=config('CLOUD_API_KEY', cast=str),
        api_secret=config('CLOUD_API_SECRET', cast=str),
        secure=True
    )
