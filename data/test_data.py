"""
Test Data Management Module

Provides centralized management of test data for automation framework.
Contains both static test data from JSON files and dynamic data generators.

Key Features:
- JSON-based test data configuration for easy maintenance
- Dynamic data generators for unique test scenarios
- Type-safe access to test data categories
- Support for user, registration, security and other test data types

Usage:
    from test_data import test_data

    # Static data
    user = test_data.valid_user
    invalid_emails = test_data.invalid_emails

    # Dynamic data
    unique_email = test_data.generate_unique_email()

Data Categories:
- users: Pre-defined user accounts for authentication tests
- registration: Email and password data for sign-up scenarios
- security: Attack patterns for security testing
- [extensible]: Add new categories as needed
"""

import json
import random
import time
from pathlib import Path
from typing import Dict, List, Any


class TestData:
    """
    Centralized test data management for automation framework.

    Combines static configuration from JSON files with dynamic data
    generation capabilities for comprehensive test coverage.

    Attributes:
        data_path (Path): Path to test_data.json configuration file
        _data (Dict): Loaded test data from JSON configuration
    """

    def __init__(self):
        self.data_path = Path(__file__).parent / "test_data.json"
        self._data = self._load_data()

    def _load_data(self) -> Dict[str, Any]:
        """
        Load test data from JSON configuration file.

        Returns:
            Dict containing all test data categories and values

        Raises:
            FileNotFoundError: If test_data.json doesn't exist
            JSONDecodeError: If JSON file is malformed
        """
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    # User Management
    @property
    def valid_user(self) -> Dict[str, str]:
        """Get valid user credentials for positive authentication tests."""
        return self._data["users"]["valid_user"]

    @property
    def admin_user(self) -> Dict[str, str]:
        """Get admin user credentials for role-based testing."""
        return self._data["users"]["admin_user"]

    # Registration Data
    @property
    def invalid_emails(self) -> List[str]:
        """Get list of invalid email formats for validation testing."""
        return self._data["registration"]["invalid_emails"]

    @property
    def weak_passwords(self) -> List[str]:
        """Get list of weak passwords for strength validation testing."""
        return self._data["registration"]["weak_passwords"]

    @property
    def strong_passwords(self) -> List[str]:
        """Get list of strong passwords for successful registration tests."""
        return self._data["registration"]["strong_passwords"]

    # Security Testing
    @property
    def sql_injection(self) -> str:
        """Get SQL injection pattern for security testing."""
        return self._data["security"]["sql_injection"]

    @property
    def xss_attempt(self) -> str:
        """Get XSS attack pattern for security testing."""
        return self._data["security"]["xss_attempt"]

    # Dynamic Data Generators
    def generate_unique_email(self, prefix: str = "test") -> str:
        """
        Generate a unique email address for registration tests.

        Args:
            prefix: Email local part prefix (default: "test")

        Returns:
            Unique email string with timestamp and random suffix
        """
        timestamp = int(time.time())
        random_suffix = random.randint(10000, 99999)
        return f"{prefix}_{timestamp}_{random_suffix}@example.com"

    def get_random_invalid_email(self) -> str:
        """
        Get random invalid email from predefined list.

        Returns:
            Random invalid email string for validation testing
        """
        return random.choice(self.invalid_emails)

    def get_random_weak_password(self) -> str:
        """
        Get random weak password from predefined list.

        Returns:
            Random weak password string for strength validation
        """
        return random.choice(self.weak_passwords)

    def reload_data(self) -> None:
        """Reload test data from JSON file (useful for runtime updates)."""
        self._data = self._load_data()


# Global singleton instance for easy access across the test framework
test_data = TestData()