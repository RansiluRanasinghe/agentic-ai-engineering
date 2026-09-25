from groq import AsyncGroq
from shared.config import Config

_async_client: AsyncGroq | None = None

def get_async_client() -> AsyncGroq:
    """
    Returns a singleton instance of the AsyncGroq client.
    Instantiates the client on the first call, then returns the cached instance.
    """
    global _async_client

    if _async_client is None:
        _async_client = AsyncGroq(
            api_key=Config.GROQ_API_KEY,
            max_retries=3,
            timeout=60.0
        )


    return _async_client    