# app/file_handler.py

"""
File Upload Handler for Media (Images & Videos)
"""

import os
import uuid
from pathlib import Path
from typing import Tuple, Optional
from fastapi import UploadFile, HTTPException, status
from PIL import Image
import io

from app.config import settings


class FileHandler:
    """Handle file uploads with validation and optimization"""

    ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'}
    ALLOWED_VIDEO_TYPES = {'video/mp4', 'video/mpeg', 'video/quicktime', 'video/x-msvideo'}

    MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB

    # Image optimization settings
    MAX_IMAGE_WIDTH = 2048
    MAX_IMAGE_HEIGHT = 2048
    IMAGE_QUALITY = 85

    @staticmethod
    def validate_file(file: UploadFile, file_type: str) -> Tuple[bool, str]:
        """
        Validate uploaded file

        Args:
            file: Uploaded file
            file_type: 'image' or 'video'

        Returns:
            Tuple of (is_valid, error_message)
        """

        # Check file type
        if file_type == 'image':
            if file.content_type not in FileHandler.ALLOWED_IMAGE_TYPES:
                return False, f"Invalid image type. Allowed: {', '.join(FileHandler.ALLOWED_IMAGE_TYPES)}"
            max_size = FileHandler.MAX_IMAGE_SIZE
        elif file_type == 'video':
            if file.content_type not in FileHandler.ALLOWED_VIDEO_TYPES:
                return False, f"Invalid video type. Allowed: {', '.join(FileHandler.ALLOWED_VIDEO_TYPES)}"
            max_size = FileHandler.MAX_VIDEO_SIZE
        else:
            return False, "Invalid file type specified"

        return True, ""

    @staticmethod
    async def save_image(file: UploadFile, subfolder: str = 'posts') -> Tuple[str, str]:
        """
        Save and optimize image file

        Args:
            file: Uploaded image file
            subfolder: Subfolder in uploads directory (posts, avatars, stories)

        Returns:
            Tuple of (file_url, file_path)
        """

        # Validate file
        is_valid, error_msg = FileHandler.validate_file(file, 'image')
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Read file content
        contents = await file.read()

        # Check size
        if len(contents) > FileHandler.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image size exceeds maximum of {FileHandler.MAX_IMAGE_SIZE / 1024 / 1024}MB"
            )

        # Generate unique filename
        file_ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        # Create directory if not exists
        upload_dir = Path(settings.UPLOAD_DIR) / subfolder
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / unique_filename

        try:
            # Open image with PIL for optimization
            image = Image.open(io.BytesIO(contents))

            # Convert RGBA to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background

            # Resize if too large
            if image.width > FileHandler.MAX_IMAGE_WIDTH or image.height > FileHandler.MAX_IMAGE_HEIGHT:
                image.thumbnail((FileHandler.MAX_IMAGE_WIDTH, FileHandler.MAX_IMAGE_HEIGHT), Image.Resampling.LANCZOS)

            # Save optimized image
            image.save(
                file_path,
                format='JPEG',
                quality=FileHandler.IMAGE_QUALITY,
                optimize=True
            )

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing image: {str(e)}"
            )

        # Return URL and path
        file_url = f"/uploads/{subfolder}/{unique_filename}"
        return file_url, str(file_path)

    @staticmethod
    async def save_video(file: UploadFile, subfolder: str = 'posts') -> Tuple[str, str]:
        """
        Save video file

        Args:
            file: Uploaded video file
            subfolder: Subfolder in uploads directory

        Returns:
            Tuple of (file_url, file_path)
        """

        # Validate file
        is_valid, error_msg = FileHandler.validate_file(file, 'video')
        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=error_msg
            )

        # Read file content
        contents = await file.read()

        # Check size
        if len(contents) > FileHandler.MAX_VIDEO_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Video size exceeds maximum of {FileHandler.MAX_VIDEO_SIZE / 1024 / 1024}MB"
            )

        # Generate unique filename
        file_ext = file.filename.split('.')[-1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_ext}"

        # Create directory if not exists
        upload_dir = Path(settings.UPLOAD_DIR) / subfolder
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / unique_filename

        # Save video file
        with open(file_path, 'wb') as f:
            f.write(contents)

        # Return URL and path
        file_url = f"/uploads/{subfolder}/{unique_filename}"
        return file_url, str(file_path)

    @staticmethod
    def delete_file(file_path: str) -> bool:
        """
        Delete a file from disk

        Args:
            file_path: Path to file

        Returns:
            True if deleted, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False


# Singleton instance
file_handler = FileHandler()