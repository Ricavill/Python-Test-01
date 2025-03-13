import logging

from starlette.responses import JSONResponse

from config.error.not_found_exception import NotFoundException
from config.error.unauthorized_exception import UnauthorizedException
from config.error.validation_exception import ValidationException

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def init_error_handlers(app):
    @app.exception_handler(ValidationException)
    def validation_exception_handler(request, exception):
        message = exception.args[0]
        logger.error(f"ValidationException: {message}")
        return JSONResponse(status_code=400, content={"message": message, "error": True})

    @app.exception_handler(UnauthorizedException)
    def unauthorized_exception_handler(request, exception):
        message = exception.args[0]
        logger.error(f"ValidationException: {message}")
        return JSONResponse(status_code=401, content={"message": message, "error": True})

    @app.exception_handler(NotFoundException)
    def not_found_exception_handler(request, exception):
        message = exception.args[0]
        logger.error(f"NotFoundException: {message}")
        return JSONResponse(status_code=404, content={"message": message, "error": True})
