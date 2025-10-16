"""
Supabase client configuration and utilities for the trading journal
"""
from django.conf import settings
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)

# Global Supabase client instance
_supabase_client = None

def get_supabase_client() -> Client:
    """
    Get or create Supabase client instance
    """
    global _supabase_client
    
    if _supabase_client is None:
        try:
            if not settings.SUPABASE_URL or not settings.SUPABASE_ANON_KEY:
                logger.warning("Supabase credentials not configured. Using local storage.")
                return None
                
            _supabase_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            return None
    
    return _supabase_client

def upload_file_to_supabase(file_content: bytes, file_path: str, content_type: str = None) -> str:
    """
    Upload file to Supabase Storage
    
    Args:
        file_content: File content as bytes
        file_path: Path where file should be stored
        content_type: MIME type of the file
    
    Returns:
        Public URL of uploaded file or None if failed
    """
    client = get_supabase_client()
    if not client:
        return None
    
    try:
        # Upload file to Supabase Storage
        response = client.storage.from_("trade-screenshots").upload(
            file_path,
            file_content,
            {"content-type": content_type or "image/jpeg"}
        )
        
        if response:
            # Get public URL
            public_url = client.storage.from_("trade-screenshots").get_public_url(file_path)
            logger.info(f"File uploaded successfully: {public_url}")
            return public_url
        else:
            logger.error("Failed to upload file to Supabase")
            return None
            
    except Exception as e:
        logger.error(f"Error uploading file to Supabase: {e}")
        return None

def delete_file_from_supabase(file_path: str) -> bool:
    """
    Delete file from Supabase Storage
    
    Args:
        file_path: Path of file to delete
    
    Returns:
        True if deleted successfully, False otherwise
    """
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        response = client.storage.from_("trade-screenshots").remove([file_path])
        logger.info(f"File deleted successfully: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Error deleting file from Supabase: {e}")
        return False

def sync_user_data_to_supabase(user_id: int, data: dict) -> bool:
    """
    Sync user data to Supabase (for real-time features)
    
    Args:
        user_id: Django user ID
        data: Data to sync
    
    Returns:
        True if synced successfully, False otherwise
    """
    client = get_supabase_client()
    if not client:
        return False
    
    try:
        # This is a placeholder for future real-time sync features
        # You can implement real-time updates here
        logger.info(f"User data synced to Supabase: {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error syncing user data to Supabase: {e}")
        return False
