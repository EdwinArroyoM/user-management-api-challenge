import uuid
import pytest


def build_user_payload(environment: str) -> dict:
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"Edwin {environment}",
        "email": f"edwin.{environment}.{unique_id}@example.com",
        "age": 30,
    }


@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_create_user_returns_201_and_created_user(session, base_url, environment):
    payload = build_user_payload(environment)

    response = session.post(f"{base_url}/{environment}/users", json=payload)

    assert response.status_code == 201

    response_body = response.json()
    assert response_body["name"] == payload["name"]
    assert response_body["email"] == payload["email"]
    assert response_body["age"] == payload["age"]