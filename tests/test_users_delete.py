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
def test_delete_user_returns_204_with_valid_auth(session, base_url, auth_token, environment):
    payload = build_user_payload(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=payload)
    assert create_response.status_code == 201

    delete_response = session.delete(
        f"{base_url}/{environment}/users/{payload['email']}",
        headers={"Authentication": auth_token},
    )

    assert delete_response.status_code == 204
    assert delete_response.text == ""