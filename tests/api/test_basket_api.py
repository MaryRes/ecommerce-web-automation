# Tests for accessing basket with and without authentication
import allure

@allure.epic("Basket API")
class TestBasketAPI:

    @allure.title("Access basket with authenticated session")
    def test_get_basket_authenticated(self, authenticated_session, basket_api_url):
        """Test accessing basket with valid session"""
        response = authenticated_session.get(basket_api_url)

        assert response.status_code == 200
        # Может возвращать пустую корзину или данные корзины

    @allure.title("Access basket without authentication")
    def test_get_basket_unauthenticated(self, unauthenticated_session, basket_api_url):
        """Test accessing basket without session"""
        response = unauthenticated_session.get(basket_api_url)

        # Может возвращать 200 (анонимная корзина) или 401/403
        assert response.status_code in [200, 401, 403]
