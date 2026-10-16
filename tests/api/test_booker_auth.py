import os

import allure
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
USERNAME = os.getenv("API_LOGIN")
PASSWORD = os.getenv("API_PASSWORD")


def send_auth_request(username, password):
    return requests.post(
        f"{BASE_URL}/auth",
        json={"username": username, "password": password},
        timeout=15,
    )


@allure.title("Successful authentication")
def test_successful_auth():
    with allure.step("Send an authentication request with valid credentials"):
        response = send_auth_request(
            username=USERNAME,
            password=PASSWORD,
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify that the token is a non-empty string"):
        response_body = response.json()
        assert "token" in response_body, response_body
        assert isinstance(response_body["token"], str), response_body
        assert response_body["token"].strip(), "Token is empty"


@allure.title("Authentication with an invalid password")
def test_login_with_invalid_password():
    with allure.step("Send an authentication request with an invalid password"):
        response = send_auth_request(
            username=USERNAME,
            password="wrongpassword",
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body


@allure.title("Authentication with an invalid username")
def test_login_with_invalid_username():
    with allure.step("Send an authentication request with an invalid username"):
        response = send_auth_request(
            username="fake@mail.com",
            password=PASSWORD,
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body


@allure.title("Authentication with an empty username")
def test_login_with_empty_login():
    with allure.step("Send an authentication request with an empty username"):
        response = send_auth_request(
            username="",
            password=PASSWORD,
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body


@allure.title("Authentication with an empty password")
def test_login_with_empty_password():
    with allure.step("Send an authentication request with an empty password"):
        response = send_auth_request(
            username=USERNAME,
            password="",
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body


@allure.title("Authentication without a username")
def test_login_without_username():
    with allure.step("Send an authentication request without the username field"):
        response = requests.post(
            url=f"{BASE_URL}/auth",
            json={"password": PASSWORD},
            timeout=15,
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body


@allure.title("Authentication without a password")
def test_login_without_password():
    with allure.step("Send an authentication request without the password field"):
        response = requests.post(
            url=f"{BASE_URL}/auth",
            json={"username": USERNAME},
            timeout=15,
        )

    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the error message and that no token is returned"):
        response_body = response.json()
        assert response_body.get("reason") == "Bad credentials", response_body
        assert "token" not in response_body, response_body