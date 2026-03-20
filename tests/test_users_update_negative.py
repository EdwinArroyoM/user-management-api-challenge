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
def test_update_nonexistent_user_returns_404(session, base_url, environment):
    missing_email = f"missing.{uuid.uuid4().hex[:8]}@example.com"

    payload = {
        "name": f"Updated {environment}",
        "email": missing_email,
        "age": 31,
    }

    response = session.put(
        f"{base_url}/{environment}/users/{missing_email}",
        json=payload,
    )

    assert response.status_code == 404


@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_update_user_with_missing_required_field_returns_400(session, base_url, environment):
    original_user = build_user_payload(environment)

    create_response = session.post(f"{base_url}/{environment}/users", json=original_user)
    assert create_response.status_code == 201

    invalid_payload = {
        "name": f"Updated {environment}",
        "email": original_user["email"],
        # Missing age on purpose
    }

    response = session.put(
        f"{base_url}/{environment}/users/{original_user['email']}",
        json=invalid_payload,
    )
    assert response.status_code == 400

@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_update_user_with_duplicate_email_returns_409(session, base_url, environment):
    first_user = build_user_payload(environment)
    second_user = build_user_payload(environment)

    first_create_response = session.post(f"{base_url}/{environment}/users", json=first_user)
    assert first_create_response.status_code == 201

    second_create_response = session.post(f"{base_url}/{environment}/users", json=second_user)
    assert second_create_response.status_code == 201

    duplicate_email_payload = {
        "name": f"Updated {environment}",
        "email": first_user["email"],
        "age": 31,
    }

    response = session.put(
        f"{base_url}/{environment}/users/{second_user['email']}",
        json=duplicate_email_payload,
    )

    assert response.status_code == 409