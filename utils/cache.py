import functools
from PIL import Image
import base64

def cache_result(func):
    """Simple caching decorator."""
    return functools.lru_cache(maxsize=None)(func)

@cache_result
def encode_image_base64(path: str) -> str:
    """Load image from path and return base64 string (cached)."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

@cache_result
def resize_image(path: str, size: tuple[int, int]) -> Image.Image:
    """Resize image and cache the result."""
    img = Image.open(path)
    return img.resize(size)
