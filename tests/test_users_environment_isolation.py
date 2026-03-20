import uuid
import pytest



def build_user_payload(environment: str) -> dict:
    unique_id = uuid.uuid4().hex[:8]

    return {
        "name": f"Edwin {environment}",
        "email": f"edwin.{environment}.{unique_id}@example.com",
        "age": 30,
    }

@pytest.mark.cross_env
@pytest.mark.xfail(reason="Known bug: cross-environment lookup returns 500 instead of 404", strict=False)
def test_user_created_in_dev_is_not_available_in_prod(session, base_url):
    payload = build_user_payload("dev")

    create_response = session.post(f"{base_url}/dev/users", json=payload)
    assert create_response.status_code == 201

    get_response = session.get(f"{base_url}/prod/users/{payload['email']}")
    assert get_response.status_code == 404

@pytest.mark.cross_env
@pytest.mark.xfail(reason="Known bug: cross-environment lookup returns 500 instead of 404", strict=False)
def test_user_created_in_prod_is_not_available_in_dev(session, base_url):
    payload = build_user_payload("prod")

    create_response = session.post(f"{base_url}/prod/users", json=payload)
    assert create_response.status_code == 201

    get_response = session.get(f"{base_url}/dev/users/{payload['email']}")
    assert get_response.status_code == 404