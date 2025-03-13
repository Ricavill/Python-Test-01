import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logging.basicConfig(
    filename='/tmp/jelou.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='a'
)

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_body = await request.body()
        logger.info(f"Request: {request.method} {request.url}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"Body: {request_body.decode('utf-8') if request_body else 'No Body'}")

        response = await call_next(request)

        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        logger.info(f"Response: {response.status_code}")
        logger.info(f"Response Body: {response_body.decode('utf-8') if response_body else 'No Body'}")

        return Response(content=response_body, status_code=response.status_code, headers=dict(response.headers),
                        media_type=response.media_type)
