# tests/test_docker_quick.py
import sys
import pytest


def test_python_version():
    """Проверяем версию Python в Docker"""
    assert sys.version_info.major == 3
    assert sys.version_info.minor == 12
    print("✅ Python 3.11 in Docker - OK")


def test_imports():
    """Проверяем что все пакеты импортируются"""
    try:
        import selenium
        import pytest
        import requests
        from webdriver_manager.chrome import ChromeDriverManager
        from dotenv import load_dotenv
        print("✅ All packages imported - OK")
        return True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_selenium_basic():
    """Базовый тест Selenium (без браузера)"""
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Проверяем что можем создать драйвер
    driver = webdriver.Chrome(options=options)
    assert driver is not None
    driver.quit()
    print("✅ Selenium WebDriver works - OK")


if __name__ == "__main__":
    test_python_version()
    test_imports()
    test_selenium_basic()
    print("🎉 DOCKER ENVIRONMENT IS READY!")