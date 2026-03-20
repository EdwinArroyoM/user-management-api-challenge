# Bugs Report

This document lists the discrepancies found between the actual API behavior and the expected behavior defined in `sdet_challenge_api.yml`.

---

## Bug 1 — GET /users/{email} returns 500 instead of 404 for a non-existent user

### Endpoint
`GET /{environment}/users/{email}`

### Expected Behavior
According to the API specification, requesting a user that does not exist should return:

- `404 Not Found`

### Actual Behavior
The API returns:

- `500 Internal Server Error`

### Environments Affected
- `dev`
- `prod`

### Evidence
Covered by:
- `tests/test_users_not_found.py`

### Impact
This breaks the documented contract for user lookup and turns a handled business case into an internal server error.

---

## Bug 2 — DELETE /users/{email} in dev allows deletion without valid authentication

### Endpoint
`DELETE /dev/users/{email}`

### Expected Behavior
According to the API specification, deleting a user without authentication or with an invalid authentication token should return:

- `401 Unauthorized`

### Actual Behavior
In the `dev` environment, the API returns:

- `204 No Content`

even when:
- the `Authentication` header is missing
- the `Authentication` header contains an invalid token

### Environments Affected
- `dev` only

### Evidence
Covered by:
- `tests/test_users_delete_negative.py`

### Impact
This is a security issue because the endpoint allows destructive actions without valid authentication in the `dev` environment. It also creates inconsistent behavior between `dev` and `prod`.

---

## Bug 3 — POST /users returns 500 instead of 409 for duplicate email

### Endpoint
`POST /{environment}/users`

### Expected Behavior
According to the API specification, creating a user with an email that already exists should return:

- `409 Conflict`

### Actual Behavior
The API returns:

- `500 Internal Server Error`

### Environments Affected
- `dev`
- `prod`

### Evidence
Covered by:
- `tests/test_users_create_negative.py`

### Impact
This breaks the documented contract for duplicate user creation and prevents clients from handling conflicts correctly.

---

## Notes
- The API specification states that `/dev` and `/prod` should expose identical behavior.
- Some negative-path scenarios do not match the documented contract and appear to be intentional defects included in the challenge.