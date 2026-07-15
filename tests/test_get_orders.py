import requests
import allure
from data import Urls, Endpoints


class TestGetOrders:
    
    @allure.title('Тест получения списка заказов')
    def test_get_orders_list(self):
        with allure.step("Отправить запрос на получение списка заказов"):
            response = requests.get(f'{Urls.BASE_URL}{Endpoints.GET_ORDERS}')
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить наличие поля orders"):
            assert 'orders' in response.json()
        
        orders = response.json()['orders']
        
        with allure.step("Проверить, что список не пустой"):
            assert isinstance(orders, list)
            assert len(orders) > 0
        
        with allure.step("Проверить структуру первого заказа"):
            first_order = orders[0]
            assert 'id' in first_order
            assert 'firstName' in first_order
            assert 'lastName' in first_order
            assert 'address' in first_order
            assert 'metroStation' in first_order
            assert 'phone' in first_order
            assert 'rentTime' in first_order
            assert 'deliveryDate' in first_order
            assert 'track' in first_order
    
    @allure.title('Тест получения списка заказов с пагинацией')
    def test_get_orders_list_with_pagination(self):
        params = {
            'limit': 5,
            'page': 0
        }
        
        with allure.step("Отправить запрос с пагинацией"):
            response = requests.get(f'{Urls.BASE_URL}{Endpoints.GET_ORDERS}', params=params)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить наличие поля orders"):
            assert 'orders' in response.json()
        
        orders = response.json()['orders']
        
        with allure.step("Проверить, что список не пустой"):
            assert isinstance(orders, list)
            assert len(orders) > 0
        
        with allure.step("Проверить, что количество заказов не превышает limit"):
            assert len(orders) <= 5