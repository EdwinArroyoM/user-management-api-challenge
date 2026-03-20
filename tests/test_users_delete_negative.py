import uuid
import pytest


def build_user_payload(environment: str) -> dict:
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"Edwin {environment}",
        "email": f"edwin.{environment}.{unique_id}@example.com",
        "age": 30,
    }

@pytest.mark.parametrize(
    "environment",
    [
        pytest.param(
            "dev",
            marks=pytest.mark.xfail(
                reason="Known bug: dev delete without auth returns 204 instead of 401",
                strict=False,
            ),
        ),
        "prod",
    ],
)
def test_delete_user_without_auth_returns_401(session, base_url, environment):
    payload = build_user_payload(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=payload)
    assert create_response.status_code == 201

    delete_response = session.delete(f"{base_url}/{environment}/users/{payload['email']}")

    assert delete_response.status_code == 401


@pytest.mark.parametrize(
    "environment",
    [
        pytest.param(
            "dev",
            marks=pytest.mark.xfail(
                reason="Known bug: dev delete with invalid auth returns 204 instead of 401",
                strict=False,
            ),
        ),
        "prod",
    ],
)
def test_delete_user_with_invalid_auth_returns_401(session, base_url, environment):
    payload = build_user_payload(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=payload)
    assert create_response.status_code == 201

    delete_response = session.delete(
        f"{base_url}/{environment}/users/{payload['email']}",
        headers={"Authentication": "invalid-token"},
    )

    assert delete_response.status_code == 401
    
@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_delete_nonexistent_user_with_valid_auth_returns_404(session, base_url, auth_token, environment):
    missing_email = f"missing.{uuid.uuid4().hex[:8]}@example.com"

    response = session.delete(
        f"{base_url}/{environment}/users/{missing_email}",
        headers={"Authentication": auth_token},
    )

    assert response.status_code == 404