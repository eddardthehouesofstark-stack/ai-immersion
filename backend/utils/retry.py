import asyncio
import functools
from typing import Callable, Any
from backend.utils.logging import get_logger

logger = get_logger("retry")

def async_retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_err = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_err = e
                    logger.warning(f"Attempt {attempt}/{max_attempts} for {func.__name__} failed: {e}")
                    if attempt == max_attempts:
                        break
                    await asyncio.sleep(current_delay)
                    current_delay *= backoff
            raise last_err
        return wrapper
    return decorator
