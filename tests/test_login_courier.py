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
        
        with allure.step("Отправить запрос на авторизацию"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверить, что в ответе есть id"):
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
        
        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 400
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.MISSING_LOGIN_DATA in response.text
    
    @allure.title('Тест авторизации с неправильным логином')
    def test_login_courier_wrong_login(self, create_courier):
        login, password, _ = create_courier
        wrong_login = generate_random_string(10)
        
        payload = {
            "login": wrong_login,
            "password": password
        }
        
        with allure.step("Отправить запрос с неправильным логином"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 404
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
    
    @allure.title('Тест авторизации с неправильным паролем')
    def test_login_courier_wrong_password(self, create_courier):
        login, password, _ = create_courier
        wrong_password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": wrong_password
        }
        
        with allure.step("Отправить запрос с неправильным паролем"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 404
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text
    
    @allure.title('Тест авторизации с несуществующим пользователем')
    def test_login_courier_nonexistent_user(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password
        }
        
        with allure.step("Отправить запрос с несуществующим пользователем"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 404
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.ACCOUNT_NOT_FOUND in response.text