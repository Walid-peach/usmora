import pytest
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_configured_origin_is_accepted(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://preview.example.test")
    configured_client = TestClient(main.create_app())

    response = configured_client.get(
        "/health", headers={"Origin": "https://preview.example.test"}
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://preview.example.test"


def test_unknown_origin_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", "https://preview.example.test")
    configured_client = TestClient(main.create_app())

    response = configured_client.get("/health", headers={"Origin": "https://unknown.example.test"})

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


def test_localhost_origin_remains_supported_by_default(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ALLOWED_ORIGINS", raising=False)
    default_client = TestClient(main.create_app())

    response = default_client.get("/health", headers={"Origin": "http://localhost:3000"})

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"


@pytest.mark.parametrize(
    "configured_origins",
    [
        "",
        "https://one.example.test,,https://two.example.test",
        "*",
        "https://preview.example.test/*",
        "https://preview.example.test/path",
        "ftp://preview.example.test",
        "localhost:3000",
    ],
)
def test_invalid_origin_entries_are_rejected(
    monkeypatch: pytest.MonkeyPatch,
    configured_origins: str,
) -> None:
    monkeypatch.setenv("ALLOWED_ORIGINS", configured_origins)

    with pytest.raises(ValueError, match="ALLOWED_ORIGINS"):
        main.create_app()


def test_health_reports_ready_without_private_data() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_reflection_returns_schema_valid_local_result() -> None:
    response = client.post(
        "/v1/reflections",
        json={
            "situation": (
                "My housemate arrived after our agreed cooking time, and I felt frustrated."
            )
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {
        "facts",
        "assumptions",
        "feelings",
        "needs",
        "draft",
        "disclaimer",
    }
    assert payload["feelings"] == ["frustrated"]
    assert payload["draft"].startswith("Hey, when")


def test_reflection_rejects_blank_situation_with_useful_error() -> None:
    response = client.post("/v1/reflections", json={"situation": "   "})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Value error, Situation cannot be empty."


def test_reflection_rejects_oversized_situation_with_useful_error() -> None:
    response = client.post("/v1/reflections", json={"situation": "x" * 4001})

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at most 4000 characters"
