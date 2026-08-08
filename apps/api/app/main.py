from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.domain.reflection import DeterministicReflectionProvider
from app.schemas import ReflectionRequest, ReflectionResponse

app = FastAPI(title="Usmora API", version="0.1.0")
provider = DeterministicReflectionProvider()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/reflections", response_model=ReflectionResponse)
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
