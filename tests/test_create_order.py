import requests
import allure
import pytest
from data import Urls, Endpoints, OrderData


class TestCreateOrder:
    
    @allure.title('Тест создания заказа с разными комбинациями цветов')
    @pytest.mark.parametrize('colors', OrderData.COLORS)
    def test_create_order_with_colors(self, colors, create_order):
        order_data = OrderData.DEFAULT.copy()
        order_data.update(colors)
        
        with allure.step(f"Отправить запрос на создание заказа с цветами {colors}"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_ORDER}', json=order_data)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 201
        
        with allure.step("Проверить наличие track в ответе"):
            assert 'track' in response.json()
            assert isinstance(response.json()['track'], int)
        
        track = response.json().get('track')
        if track:
            with allure.step("Отменить заказ для очистки"):
                requests.put(f'{Urls.BASE_URL}{Endpoints.CANCEL_ORDER}', json={'track': track})