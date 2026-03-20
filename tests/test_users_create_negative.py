import uuid
import pytest


def build_user_payload(environment: str) -> dict:
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"Edwin {environment}",
        "email": f"edwin.{environment}.{unique_id}@example.com",
        "age": 30,
    }

@pytest.mark.xfail(reason="Known bug: duplicate email returns 500 instead of 409", strict=False)
@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_create_user_with_duplicate_email_returns_409(session, base_url, environment):
    payload = build_user_payload(environment)

    first_response = session.post(f"{base_url}/{environment}/users", json=payload)
    assert first_response.status_code == 201

    second_response = session.post(f"{base_url}/{environment}/users", json=payload)

    assert second_response.status_code == 409


@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_create_user_with_missing_required_field_returns_400(session, base_url, environment):
    invalid_payload = {
        "name": f"Edwin {environment}",
        "email": f"invalid.{uuid.uuid4().hex[:8]}@example.com",
        # Missing age on purpose to catch the 400 error
    }

    response = session.post(f"{base_url}/{environment}/users", json=invalid_payload)

    assert response.status_code == 400