import pytest
from api.registration import UserRegistration
import test_data

registration = UserRegistration()


def test_register_user():
    password = test_data.valid_reg_password
    confirmation_link, email, body, status = registration.register_user_with_generated_email(password)
    assert confirmation_link is not None
    assert email is not None
    assert status == 200, f"Expected status 200, received {status} during registration"
    assert body['detail']['message'] == "Please, visit your email to confirm registration"


@pytest.mark.parametrize('email', test_data.invalid_reg_emails)
def test_register_user_with_invalid_email(email):
    email, body, status = registration.register_user_with_predefined_email(email)
    assert status == 422, f"Expected status 422, received {status} during registration with invalid email"
    messages = ["none is not an allowed value", "value is not a valid email address"]
    assert body['detail'][0]['msg'] in messages


@pytest.mark.parametrize('password', test_data.invalid_reg_passwords)
def test_register_user_with_invalid_password(password):
    _, email, body, status = registration.register_user_with_generated_email(password)
    assert status == 422, f"Expected status 422, received {status} during registration with invalid password"
    assert 'detail' in body
    error_detail = body['detail'][0]
    assert error_detail['loc'] == ['body', 'password']


def test_register_user_with_existing_email():
    password = test_data.valid_reg_password
    # 1. Registration of a new user
    _, email, body, status = registration.register_user_with_generated_email(password)
    assert status == 200, f"Expected status 200, received {status} during registration"

    # 2. Attempt to re-register with the same email
    email, body, status = registration.register_user_with_predefined_email(email)
    assert status in [400, 409], f"Expected status 400 or 409, but received {status} during re-registration"
    assert body['detail'] == "Email is already registered", f"Incorrect error message: {body['detail']}"


def test_confirm_email():
    password = test_data.valid_reg_password
    registration.register_user_with_generated_email(password)
    reg_token, status, body = registration.confirm_email()
    assert reg_token is not None
    assert status == 200, f"Expected status 200, received {status}"
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"


def test_send_personal_info():
    password = test_data.valid_reg_password
    registration.register_user_with_generated_email(password)
    registration.confirm_email()
    status, body = registration.send_personal_info()
    assert status == 200, f"Expected status 200, received {status}"
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"


def test_send_business_info():
    password = test_data.valid_reg_password
    registration.register_user_with_generated_email(password)
    registration.confirm_email()
    registration.send_personal_info()
    status, body = registration.send_business_info()
    assert status == 200, f"Expected status 200, received {status}"
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"


def test_delete_user():
    password = test_data.valid_reg_password
    registration.register_user_with_generated_email(password)
    registration.confirm_email()
    status, body = registration.delete_user()
    assert status == 200
    assert body['result'] is True, f"Expected 'result' to be True, but got {body['result']}"


def test_e2e_registration_and_setup_account():
    password = test_data.valid_reg_password
    confirmation_link, email, body, status = registration.register_user_with_generated_email(password)
    assert confirmation_link is not None
    assert email is not None
    assert status == 200
    assert body['detail']['message'] == "Please, visit your email to confirm registration"

    reg_token, status, body = registration.confirm_email()
    assert reg_token is not None
    assert status == 200
    assert body['result'] is True

    status, body = registration.send_personal_info()
    assert status == 200
    assert body['ok'] is True
    assert body['result'] is True

    status, body = registration.send_business_info()
    assert status == 200
    assert body['result'] is True
