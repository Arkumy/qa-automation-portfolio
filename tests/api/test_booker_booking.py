import allure
import pytest
import requests

from config import BASE_URL, USERNAME, PASSWORD

@pytest.fixture
def created_booking_id():
    with allure.step("Create a booking for the test"):
        response = requests.post(
            url=f"{BASE_URL}/booking",
            json=booking_data,
            timeout=15,
        )
        assert response.status_code == 200, response.text

        response_body = response.json()
        assert "bookingid" in response_body, response_body
        assert isinstance(response_body["bookingid"], int), response_body
        assert response_body["bookingid"] > 0, response_body

    return response_body["bookingid"]


@pytest.fixture
def auth_token():
    with allure.step("Create a token for the test"):
        response = requests.post(
            url=f"{BASE_URL}/auth",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=15,
        )
        assert response.status_code == 200, response.text

        response_body = response.json()
        assert "token" in response_body, response_body
        assert isinstance(response_body["token"], str), response_body
        assert response_body["token"].strip(), "Auth token is empty"
    return response_body["token"]


booking_data = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 240,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2026-11-10",
        "checkout": "2026-11-21"
    },
    "additionalneeds": "Breakfast"
}


@allure.title("Successful booking creation")
def test_create_booking():
    with allure.step("Send a booking creation request"):
        response = requests.post(
            url=f"{BASE_URL}/booking",
            json=booking_data,
            timeout=15,
        )
    with allure.step("Verify HTTP status code 200"):
        assert response.status_code == 200, response.text

    with allure.step("Verify the booking ID"):
        response_body = response.json()
        assert "bookingid" in response_body, response_body
        assert isinstance(response_body["bookingid"], int), response_body
        assert response_body["bookingid"] > 0, response_body

    with allure.step("Verify the returned booking data"):
        assert response_body["booking"] == booking_data, response_body


@allure.title("Successful booking retrieval")
def test_get_booking_by_id(created_booking_id):
    with allure.step("Get the booking by ID"):
        response = requests.get(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            timeout=15
        )

    with allure.step("Verify the returned booking data"):
        assert response.status_code == 200, response.text
        response_body = response.json()
        assert response_body == booking_data, response_body


@allure.title("Get the booking by invalid ID")
def test_get_booking_by_invalid_id():
    with allure.step("Get the booking by invalid ID"):
        response = requests.get(
            url=f"{BASE_URL}/booking/0",
            timeout=15
        )
    with allure.step("Verify the status code"):
        assert response.status_code == 404, response.text
        response_body = response.text
        assert response_body == "Not Found", response_body


updated_booking_data = {
    "firstname": "Betty",
    "lastname": "Brett",
    "totalprice": 300,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2026-11-20",
        "checkout": "2026-11-25"
    },
    "additionalneeds": "Private shower"
}


@allure.title("Successful booking update")
def test_change_booking(created_booking_id, auth_token):
    with allure.step("Send a booking update request"):
        response = requests.put(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            json=updated_booking_data,
            timeout=15,
            headers={"Cookie": f"token={auth_token}"},
        )

    with allure.step("Verify the update response"):
        assert response.status_code == 200, response.text
        response_body = response.json()
        assert response_body == updated_booking_data, response_body

    with allure.step("Verify that the booking changes are saved"):
        response = requests.get(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            timeout=15
        )
        assert response.status_code == 200, response.text
        response_body = response.json()
        assert response_body == updated_booking_data, response_body


@allure.title("Successful partial booking update")
def test_update_data(created_booking_id, auth_token):
    with allure.step("Send a booking update request"):
        response = requests.patch(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            json={
                "firstname": "Alice",
                "lastname": "Smith"},
            timeout=14,
            headers={"Cookie": f"token={auth_token}"}
        )

    with allure.step("Verify the update response"):
        assert response.status_code == 200, response.text
        response_body = response.json()
    with allure.step("Verify the updated and unchanged booking fields"):
        assert response_body["firstname"] == "Alice", response_body
        assert response_body["lastname"] == "Smith", response_body
        assert response_body["totalprice"] == booking_data["totalprice"], response_body
        assert response_body["bookingdates"] == booking_data["bookingdates"], response_body
        assert response_body["additionalneeds"] == booking_data["additionalneeds"], response_body
        assert response_body["depositpaid"] == booking_data["depositpaid"], response_body

    with allure.step("Verify the retrieval response"):
        response = requests.get(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            timeout=15
        )

    with allure.step("Verify the update response"):
        assert response.status_code == 200, response.text
        response_body = response.json()
    with allure.step("Verify the updated data"):
        assert response_body["firstname"] == "Alice", response_body
        assert response_body["lastname"] == "Smith", response_body


@allure.title("Delete booking")
def test_delete_booking(created_booking_id, auth_token):
    with allure.step("Send a booking delete request"):
        response = requests.delete(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            timeout=14,
            headers={"Cookie": f"token={auth_token}"}
        )

    with allure.step("Verify the delete response"):
        assert response.status_code == 201, response.text
    with allure.step("Get the booking after deletion"):
        response = requests.get(
            url=f"{BASE_URL}/booking/{created_booking_id}",
            timeout=15
        )

    with allure.step("Verify that the booking was deleted"):
        assert response.status_code == 404, response.text
        response_body = response.text
        assert response_body == "Not Found", response_body

