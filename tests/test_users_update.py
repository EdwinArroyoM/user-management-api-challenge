import uuid
import pytest


def build_original_user(environment: str) -> dict:
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"Edwin {environment}",
        "email": f"edwin.{environment}.{unique_id}@example.com",
        "age": 30,
    }


def build_updated_user(original_email: str, environment: str) -> dict:
    return {
        "name": f"Edwin Updated {environment}",
        "email": original_email,
        "age": 31,
    }


@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_update_user_returns_200_and_updated_user(session, base_url, environment):
    original_user = build_original_user(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=original_user)
    assert create_response.status_code == 201

    updated_user = build_updated_user(original_user["email"], environment)

    update_response = session.put(
        f"{base_url}/{environment}/users/{original_user['email']}",
        json=updated_user,
    )
    assert update_response.status_code == 200

    response_body = update_response.json()
    assert response_body["name"] == updated_user["name"]
    assert response_body["email"] == updated_user["email"]
    assert response_body["age"] == updated_user["age"]