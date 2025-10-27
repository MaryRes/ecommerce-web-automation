# tests/api/conftest.py
import pytest
import requests
from data.data_manager import data_manager
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def api_session():
    """Session for API tests with common headers"""
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'User-Agent': 'QA-Tests/1.0'
    })
    logger.info("Created new API session with default headers")
    yield session
    session.close()
    logger.info("Closed API session")


@pytest.fixture
def authenticated_session(api_session, login_api_url):
    """This API uses session-based authentication (not tokens)"""

    # 🔴 ПРОБЛЕМА: используем email, но API ожидает username
    # 🟢 РЕШЕНИЕ: используем username или создаем его в test_data

    login_data = {
        "username": data_manager.valid_user["email"],  # 🎉 НАЙДЕНО!
        "password": data_manager.valid_user["password"]          # 🎉 НАЙДЕНО!
    }
    logger.info(f"Attempting login with username: {login_data['username']}")

    response = api_session.post(login_api_url, json=login_data)

    assert response.status_code == 200, (
        f"Login failed with status {response.status_code}. "
        f"Response: {response.text}. "
        f"Used username: {login_data['username']}"
    )

    # Проверяем что сессия создана
    if 'sessionid' in api_session.cookies:
        logger.info("✅ Session authenticated successfully with sessionid cookie")
    else:
        logger.warning("⚠️  Login successful but no sessionid cookie found")

    return api_session


@pytest.fixture
def unauthenticated_session(api_session):
    """Session without authentication for negative tests"""
    return api_session


@pytest.fixture
def login_payload():
    """Provide correct login payload structure"""
    return {
        "username": data_manager.valid_user["username"],  # ← put real username
        "password": data_manager.valid_user["password"]  # ← put real password
    }


# Debug fixture to trace authentication steps
@pytest.fixture
def debug_session(api_session, login_api_url):
    """Debug fixture to check authentication process"""
    print("\n=== DEBUG SESSION ===")
    print(f"Initial cookies: {dict(api_session.cookies)}")

    test_credentials = [
        {"username": "admin", "password": "test"},
        {"username": "test", "password": "test"},
        {"username": "user", "password": "test"},
    ]

    for creds in test_credentials:
        print(f"Trying: {creds}")
        response = api_session.post(login_api_url, json=creds)
        print(f"Status: {response.status_code}, Cookies: {dict(api_session.cookies)}")

        if response.status_code == 200:
            print("✅ SUCCESS! Using these credentials")
            return api_session

    print("❌ No working credentials found")
    return api_session


# Дополнительные фикстуры для разных тестовых сценариев
@pytest.fixture
def invalid_credentials_payload():
    """Payload with invalid credentials for negative tests"""
    return {
        "username": "invalid_user",
        "password": "wrong_password"
    }


@pytest.fixture
def empty_credentials_payload():
    """Payload with empty credentials"""
    return {
        "username": "",
        "password": ""
    }