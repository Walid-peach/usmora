import os
from urllib.parse import urlsplit

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.domain.reflection import DeterministicReflectionProvider
from app.schemas import ReflectionRequest, ReflectionResponse

DEFAULT_ALLOWED_ORIGIN = "http://localhost:3000"
provider = DeterministicReflectionProvider()


def allowed_origins() -> list[str]:
    configured = os.environ.get("ALLOWED_ORIGINS")
    if configured is None:
        return [DEFAULT_ALLOWED_ORIGIN]

    origins = [origin.strip() for origin in configured.split(",")]
    for origin in origins:
        if not origin:
            raise ValueError("ALLOWED_ORIGINS must not contain blank entries")
        if "*" in origin:
            raise ValueError("ALLOWED_ORIGINS must contain exact origins, not wildcards")
        if any(character.isspace() for character in origin):
            raise ValueError("ALLOWED_ORIGINS must contain exact HTTP(S) origins")
        try:
            parsed = urlsplit(origin)
            hostname = parsed.hostname
            port = parsed.port
        except ValueError as exc:
            raise ValueError("ALLOWED_ORIGINS must contain valid HTTP(S) origins") from exc
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or hostname is None
            or parsed.username is not None
            or parsed.password is not None
            or parsed.path
            or parsed.query
            or parsed.fragment
            or (port is not None and not 0 <= port <= 65535)
        ):
            raise ValueError("ALLOWED_ORIGINS must contain exact HTTP(S) origins")
    return origins


def create_app() -> FastAPI:
    application = FastAPI(title="Usmora API", version="0.1.0")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins(),
        allow_credentials=False,
        allow_methods=["POST", "GET"],
        allow_headers=["Content-Type"],
    )

    @application.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @application.post("/v1/reflections", response_model=ReflectionResponse)
    def create_reflection(request: ReflectionRequest) -> ReflectionResponse:
        result = provider.reflect(request.situation)
        return ReflectionResponse(
            facts=result.facts,
            assumptions=result.assumptions,
            feelings=result.feelings,
            needs=result.needs,
            draft=result.draft,
            disclaimer=result.disclaimer,
        )

    return application


app = create_app()
