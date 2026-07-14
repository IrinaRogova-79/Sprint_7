import requests
import allure
import pytest
from data import BASE_URL, ORDER_DATA, COLORS_DATA, CREATE_ORDER_ENDPOINT, CANCEL_ORDER_ENDPOINT


class TestCreateOrder:
    
    @allure.title('Тест создания заказа с разными комбинациями цветов')
    @pytest.mark.parametrize('colors', COLORS_DATA)
    def test_create_order_with_colors(self, colors):
        order_data = ORDER_DATA.copy()
        order_data.update(colors)
        
        response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        assert isinstance(response.json()['track'], int)
        
        track = response.json().get('track')
        if track:
            requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})
    
    @allure.title('Тест создания заказа с цветом BLACK')
    def test_create_order_with_black_color(self):
        order_data = ORDER_DATA.copy()
        order_data.update({"colors": ["BLACK"]})
        
        response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json().get('track')
        if track:
            requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})
    
    @allure.title('Тест создания заказа с цветом GREY')
    def test_create_order_with_grey_color(self):
        order_data = ORDER_DATA.copy()
        order_data.update({"colors": ["GREY"]})
        
        response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json().get('track')
        if track:
            requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})
    
    @allure.title('Тест создания заказа с двумя цветами')
    def test_create_order_with_both_colors(self):
        order_data = ORDER_DATA.copy()
        order_data.update({"colors": ["BLACK", "GREY"]})
        
        response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json().get('track')
        if track:
            requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})
    
    @allure.title('Тест создания заказа без указания цвета')
    def test_create_order_without_color(self):
        order_data = ORDER_DATA.copy()
        
        response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=order_data)
        
        assert response.status_code == 201
        assert 'track' in response.json()
        
        track = response.json().get('track')
        if track:
            requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})