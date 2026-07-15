import requests
import allure
import pytest
from data import Urls, Endpoints, ErrorMessages
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestLoginCourier:
    
    @allure.title('Тест успешной авторизации курьера')
    def test_login_courier_success(self, create_courier):
        login, password, _ = create_courier
    
        payload = {
            "login": login,
            "password": password
        }
    
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
    
        assert response.status_code == 200
        assert 'id' in response.json()
        assert isinstance(response.json()['id'], int)
    
    @allure.title('Тест авторизации без обязательного поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_login_courier_missing_field(self, create_courier, missing_field):
        login, password, _ = create_courier
    
        payload = {
            "login": login,
            "password": password
        }
    
        del payload[missing_field]
    
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        assert response.status_code == 400
        assert ErrorMessages.MISSING_LOGIN_DATA in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации с неправильным логином')
    def test_login_courier_wrong_login(self, create_courier):
        login, password, _ = create_courier
        wrong_login = generate_random_string(10)
    
        payload = {
            "login": wrong_login,
            "password": password
        }
    
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        assert response.status_code == 404
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест авторизации с неправильным паролем')
    def test_login_courier_wrong_password(self, create_courier):
        login, password, _ = create_courier
        wrong_password = generate_random_string(10)
    
        payload = {
            "login": login,
            "password": wrong_password
        }
    
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        assert response.status_code == 404
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
        
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
        
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        assert response.status_code == 400
        assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text