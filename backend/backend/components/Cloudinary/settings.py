from os import environ

import cloudinary

# Cloudinary
cloudinary.config(
    cloud_name=environ.get('CLOUD_NAME'),
    api_key=environ.get('CLOUD_API_KEY'),
    api_secret=environ.get('CLOUD_API_SECRET'),
    secure=True
)
