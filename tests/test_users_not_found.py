import uuid
import pytest


@pytest.mark.xfail(reason="Known bug: GET nonexistent user returns 500 instead of 404", strict=False)
@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_get_nonexistent_user_returns_404(session, base_url, environment):
    missing_email = f"missing.{uuid.uuid4().hex[:8]}@example.com"

    response = session.get(f"{base_url}/{environment}/users/{missing_email}")

    assert response.status_code == 404