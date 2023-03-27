from django.conf import settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


def create_application(django_app) -> FastAPI:
    from crawler.api import register_routers
    from optifino.throttling import limiter

    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.ALLOWED_HOSTS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_routers(app, prefix='/api/crawler')

    return app
