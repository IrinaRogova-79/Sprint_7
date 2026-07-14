import requests
import allure
import pytest
from data import BASE_URL, LOGIN_COURIER_ENDPOINT
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestLoginCourier:
    
    @allure.title('Тест успешной авторизации курьера')
    def test_login_courier_success(self, create_courier):
        login, password, _ = create_courier
    
        payload = {
            "login": login,
            "password": password
        }
    
        response = requests.post(f'{BASE_URL}{LOGIN_COURIER_ENDPOINT}', data=payload)
    
        assert response.status_code == 200
        assert 'id' in response.json()
        assert isinstance(response.json()['id'], int)
        
        courier_id = response.json().get('id')
        if courier_id:
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации без обязательного поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_missing_field(self, missing_field):
        courier_data = register_new_courier_and_return_login_password()
        
        if not courier_data:
            pytest.skip("Не удалось создать курьера")
        
        login, password = courier_data[0], courier_data[1]
        
        payload = {
            "login": login,
            "password": password
        }
        
        del payload[missing_field]
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        if response.status_code == 504:
            pytest.skip("Сервер временно недоступен (504 Gateway Timeout)")
        
        assert response.status_code == 400
        assert "Недостаточно данных для входа" in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации с неправильным логином')
    def test_login_courier_wrong_login(self):
        courier_data = register_new_courier_and_return_login_password()
        
        if not courier_data:
            pytest.skip("Не удалось создать курьера")
        
        login, password = courier_data[0], courier_data[1]
        
        wrong_login = generate_random_string(10)
        
        payload = {
            "login": wrong_login,
            "password": password
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        if response.status_code == 504:
            pytest.skip("Сервер временно недоступен (504 Gateway Timeout)")
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации с неправильным паролем')
    def test_login_courier_wrong_password(self):
        courier_data = register_new_courier_and_return_login_password()
        
        if not courier_data:
            pytest.skip("Не удалось создать курьера")
        
        login, password = courier_data[0], courier_data[1]
        
        wrong_password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": wrong_password
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        if response.status_code == 504:
            pytest.skip("Сервер временно недоступен (504 Gateway Timeout)")
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации с несуществующим пользователем')
    def test_login_courier_nonexistent_user(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)
        
        if response.status_code == 504:
            pytest.skip("Сервер временно недоступен (504 Gateway Timeout)")
        
        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.text