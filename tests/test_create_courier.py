import requests
import allure
import pytest
from data import Urls, Endpoints, ErrorMessages
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestCreateCourier:
    
    @allure.title('Тест создания нового курьера')
    def test_create_courier_success(self, delete_courier_after_test):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        with allure.step("Отправить запрос на создание курьера"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 201
        
        with allure.step("Проверить тело ответа"):
            assert response.json() == {"ok": True}
        
        delete_courier_after_test(login, password)
    
    @allure.title('Тест создания двух одинаковых курьеров')
    def test_create_duplicate_courier(self, create_courier, delete_courier_after_test):
        login, password, first_name = create_courier
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        with allure.step("Отправить запрос на создание дубликата курьера"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 409
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.DUPLICATE_LOGIN in response.text
    
    @allure.title('Тест создания курьера без обязательного поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field, delete_courier_after_test):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        del payload[missing_field]
        
        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 400
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.MISSING_DATA in response.text
        
        if missing_field != 'login':
            delete_courier_after_test(login, password)
    
    @allure.title('Тест создания курьера с существующим логином')
    def test_create_courier_existing_login(self, create_courier, delete_courier_after_test):
        login, password, _ = create_courier
        
        new_password = generate_random_string(10)
        new_first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": new_password,
            "firstName": new_first_name
        }
        
        with allure.step("Отправить запрос на создание курьера с существующим логином"):
            response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_COURIER}', data=payload)
        
        with allure.step("Проверить код ответа"):
            assert response.status_code == 409
        
        with allure.step("Проверить сообщение об ошибке"):
            assert ErrorMessages.DUPLICATE_LOGIN in response.text