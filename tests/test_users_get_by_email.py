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
def test_get_user_by_email_returns_200_and_expected_user(session, base_url, environment):
    payload = build_user_payload(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=payload)
    assert create_response.status_code == 201

    get_response = session.get(f"{base_url}/{environment}/users/{payload['email']}")
    assert get_response.status_code == 200

    response_body = get_response.json()
    assert response_body["name"] == payload["name"]
    assert response_body["email"] == payload["email"]
    assert response_body["age"] == payload["age"]