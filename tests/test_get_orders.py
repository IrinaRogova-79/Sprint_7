import requests
import allure
from data import BASE_URL, GET_ORDERS_ENDPOINT

class TestGetOrders:
    
    @allure.title('Тест получения списка заказов')
    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}{GET_ORDERS_ENDPOINT}')
    
        assert response.status_code == 200
        assert 'orders' in response.json()
    
        orders = response.json()['orders']
        assert isinstance(orders, list)
    
        if len(orders) > 0:
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
        
        response = requests.get(f'{BASE_URL}/api/v1/orders', params=params)
        
        assert response.status_code == 200
        assert 'orders' in response.json()
        
        orders = response.json()['orders']
        assert isinstance(orders, list)
        
        if len(orders) > 0:
            assert len(orders) <= 5