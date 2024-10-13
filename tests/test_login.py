import pytest
import settings
from api.login import UserLogin
import test_data

login = UserLogin()


def test_user_login():
    access_token, status, body = login.user_login()
    assert access_token is not None
    assert status == 200, f"Expected status 200, received {status} during login"
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"


@pytest.mark.parametrize('email', test_data.invalid_login_emails)
def test_user_login_with_invalid_email(email):
    password = settings.PASSWORD
    access_token, status, body = login.user_login(email, password)
    assert access_token is None
    expected_status_codes = [403, 422]
    assert status in expected_status_codes, f"Expected status 403 or 422, received {status} during login"
    if status == 403:
        assert body['detail'] == "Wrong email or password, maybe email was not confirmed or account was deleted?"
    elif status == 422:
        assert body['detail'][0]['msg'] == 'value is not a valid email address'


@pytest.mark.parametrize('password', test_data.invalid_login_passwords)
def test_user_login_with_invalid_password(password):
    email = settings.SUPPLIER_EMAIL
    access_token, status, body = login.user_login(email, password)
    assert access_token is None
    assert status == 403, f"Expected status 403, received {status} during login"
    assert body['detail'] == "Wrong email or password, maybe email was not confirmed or account was deleted?"


def test_user_logout():
    login.user_login()
    status, body = login.user_logout()
    assert status == 200, f"Expected status 200, received {status} during logout"
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"
