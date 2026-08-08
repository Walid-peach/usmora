from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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
