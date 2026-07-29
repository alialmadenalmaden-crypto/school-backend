import os
import cloudinary
import cloudinary.uploader
from typing import Optional, Union, BinaryIO

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "urbrvnqi")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "795397444597679")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "ZMud54JeTNIB6m9dOfJSkjVoc44")

# Check if Cloudinary is fully configured in the environment variables
IS_CLOUDINARY_CONFIGURED = bool(CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)

if IS_CLOUDINARY_CONFIGURED:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )
    print("Cloudinary successfully configured for cloud image storage.")
else:
    print("Cloudinary variables missing. Using local file storage fallback.")

def upload_image_to_cloudinary(file: Union[BinaryIO, bytes, str], folder: str = "platform_images") -> Optional[str]:
    """
    Upload an image (file object, raw bytes, or base64 data string) to Cloudinary.
    Returns the secure URL string if successful, otherwise None.
    """
    if not IS_CLOUDINARY_CONFIGURED:
        return None
    try:
        # Rewind file-like object stream if possible
        if hasattr(file, 'seek'):
            try:
                file.seek(0)
            except Exception:
                pass
        
        upload_result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="image"
        )
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Cloudinary upload error: {str(e)}")
        return None
