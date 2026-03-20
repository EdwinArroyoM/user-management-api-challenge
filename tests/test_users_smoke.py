import pytest


@pytest.mark.parametrize("environment", ["dev", "prod"])
def test_get_users_returns_200_and_json_array(session, base_url, environment):
    response = session.get(f"{base_url}/{environment}/users")

    assert response.status_code == 200

    response_body = response.json()
    assert isinstance(response_body, list)