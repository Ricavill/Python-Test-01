from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from config.auth.__init import SECRET_KEY
from utils.jwt_utils import decode_token


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        public_routes = ["/api/users/login", "/"]
        # Check if the request path exists in the app's routes
        route_exists = any(route.path == request.url.path for route in request.app.router.routes)

        if not route_exists:
            return await call_next(request)  # Skip authentication for 404 paths
        
        if request.url.path in public_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = auth_header.split(" ")[1]  # Extract token

        user = decode_token(token, SECRET_KEY)
        request.state.user = user
        return await call_next(request)
