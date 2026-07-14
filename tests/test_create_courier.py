import requests
import allure
import pytest
from data import BASE_URL
from helpers import generate_random_string, register_new_courier_and_return_login_password


class TestCreateCourier:
    
    @allure.title('Тест создания нового курьера')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}
    
    @allure.title('Тест создания двух одинаковых курьеров')
    def test_create_duplicate_courier(self, create_courier):
        login, password, first_name = create_courier
    
     payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
    
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')
    
    @allure.title('Тест создания курьера без обязательного поля')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_missing_field(self, missing_field):
        payload = {
            "login": generate_random_string(10),
            "password": generate_random_string(10),
            "firstName": generate_random_string(10)
        }
        
        del payload[missing_field]
        
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        
        assert response.status_code == 400
        assert "Недостаточно данных для создания учетной записи" in response.text
    
    @allure.title('Тест создания курьера с существующим логином')
    def test_create_courier_existing_login(self, create_courier):
        login, password, _ = create_courier
    
        new_password = generate_random_string(10)
        new_first_name = generate_random_string(10)
    
        payload = {
            "login": login,
            "password": new_password,
            "firstName": new_first_name
        }
    
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
    
        assert response.status_code == 409
        assert "Этот логин уже используется" in response.text
        
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', 
                                      data={"login": login, "password": password})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')