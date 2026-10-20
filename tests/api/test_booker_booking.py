import os

import allure
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")


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
