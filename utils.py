import hashlib

async def generate_hash(original_url: str) -> str:
    """
    Generate a unique hash for the given URL.
    This is a placeholder function. In a real application, you would implement
    a proper hashing algorithm or use a library to generate unique hashes.
    """
    return hashlib.md5(original_url.encode()).hexdigest()[:6]