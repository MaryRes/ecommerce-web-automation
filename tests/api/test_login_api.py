## tests/api/test_login_api.py
import allure
import pytest
import json
from data.api_endpoints import API_ENDPOINTS
from data.data_manager import data_manager as test_data


# Tests for session-based login API

@allure.epic("Authentication API")
@allure.feature("Session-based Login")
class TestLoginAPI:

    @allure.title("Successful login with valid credentials")
    def test_login_success(self, authenticated_session, login_api_url):
        """Test successful session-based login"""

        with allure.step("Verify session is active by accessing protected endpoint"):
            basket_response = authenticated_session.get(API_ENDPOINTS['basket'])
            allure.attach(f"Status: {basket_response.status_code}", name="Basket Access",
                          attachment_type=allure.attachment_type.TEXT)
            assert basket_response.status_code == 200

    @allure.title("Login with valid credentials returns 200")
    def test_login_returns_200(self, api_session, login_api_url):
        """Test login endpoint returns 200 on success"""
        payload = {
            "username": test_data.valid_user["username"],
            "password": test_data.valid_user["password"]
        }

        with allure.step("Send login request"):
            response = api_session.post(login_api_url, json=payload)
            allure.attach(str(payload), name="Request Payload", attachment_type=allure.attachment_type.JSON)
            allure.attach(f"Status: {response.status_code}", name="Response Status",
                          attachment_type=allure.attachment_type.TEXT)

        with allure.step("Verify successful response"):
            assert response.status_code == 200
            assert 'sessionid' in api_session.cookies

    @allure.title("Login with invalid credentials validation")
    @pytest.mark.parametrize("test_case", test_data.login_validation_cases)
    def test_login_validation(self, api_session, login_api_url, test_case):
        """Test login validation with various invalid credential scenarios"""

        with allure.step(f"Test: {test_case['name']}"):
            allure.dynamic.title(f"Login validation: {test_case['name']}")


            test_data = {
                "username": test_case["username"],
                "password": test_case["password"]
            }

            # Attach test case info
            allure.attach(
                json.dumps(test_case, indent=2),
                name="Test Case Details",
                attachment_type=allure.attachment_type.JSON
            )

            # Send login request
            response = api_session.post(login_api_url, json=test_data)

            # Attach request/response
            allure.attach(
                json.dumps(test_data, indent=2),
                name="Request Data",
                attachment_type=allure.attachment_type.JSON
            )
            allure.attach(
                f"Status: {response.status_code}\nResponse: {response.text}",
                name="Response Info",
                attachment_type=allure.attachment_type.TEXT
            )

            # Check response status and cookies
            assert response.status_code == 401, (
                f"Expected 401 for {test_case['name']}, got {response.status_code}"
            )
            assert 'sessionid' not in api_session.cookies

            # Additional checks based on expected error type
            response_text = response.text.lower()

            if test_case["expected_error"] == "blank_email":
                assert "blank" in response_text or "empty" in response_text
            elif test_case["expected_error"] == "invalid_email":
                assert "invalid" in response_text or "valid" in response_text
            elif test_case["expected_error"] == "invalid_credentials":
                assert "invalid login" in response_text or "credentials" in response_text

    @allure.title("Login with SQL injection protection")
    def test_sql_injection_protection(self, api_session, login_api_url):
        """Test SQL injection protection in username field"""
        sql_payload = {
            "username": "' OR '1'='1",
            "password": "any_password"
        }

        response = api_session.post(login_api_url, json=sql_payload)

        # Should not return 500 error
        assert response.status_code != 500
        assert response.status_code in [400, 401]

    @allure.title("Login with empty credentials validation")
    def test_login_empty_credentials(self, api_session, login_api_url):
        """Test validation for empty credentials"""
        empty_payload = {
            "username": "",
            "password": ""
        }

        response = api_session.post(login_api_url, json=empty_payload)

        assert response.status_code == 401
        response_data = response.json()
        assert "blank" in str(response_data).lower()

    @allure.title("Logout functionality - Strict verification")
    def test_logout_strict(self, authenticated_session, login_api_url):
        """Test logout with strict verification of anonymous basket"""

        with allure.step("Get authenticated basket"):
            basket_before = authenticated_session.get(API_ENDPOINTS['basket'])
            basket_data_before = basket_before.json()
            basket_id_before = basket_data_before.get('id')

        with allure.step("Perform logout"):
            csrf_token = authenticated_session.cookies.get('csrftoken')
            logout_response = authenticated_session.delete(
                login_api_url,
                headers={'X-CSRFToken': csrf_token} if csrf_token else {}
            )
            assert logout_response.status_code in [200, 204]

        with allure.step("Verify anonymous basket properties"):
            basket_after = authenticated_session.get(API_ENDPOINTS['basket'])
            basket_data_after = basket_after.json()

            # Check that we have a different basket now
            assert basket_data_after.get('id') != basket_id_before

            # Check that the new basket is empty
            assert basket_data_after.get('total_excl_tax') == '0.00'
            # Check that the lines URL is correct for the new basket
            assert basket_data_after.get(
                'lines') == "http://selenium1py.pythonanywhere.com/api/baskets/{}/lines/".format(
                basket_data_after.get('id')
            )


