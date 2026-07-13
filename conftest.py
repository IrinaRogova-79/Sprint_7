import pytest
import requests
from helpers import register_new_courier_and_return_login_password


@pytest.fixture
def create_courier():
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        login, password = login_pass[0], login_pass[1]
        response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/courier/login', 
                                 data={'login': login, 'password': password})
        if response.status_code == 200:
            courier_id = response.json().get('id')
            if courier_id:
                requests.delete(f'https://qa-scooter.praktikum-services.ru/api/v1/courier/{courier_id}')


@pytest.fixture
def create_order():
    order_data = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Test Address",
        "metroStation": 1,
        "phone": "+79998887766",
        "rentTime": 5,
        "deliveryDate": "2026-07-15",
        "comment": "Test order"
    }
    response = requests.post('https://qa-scooter.praktikum-services.ru/api/v1/orders', json=order_data)
    track = response.json().get('track')
    yield order_data, track
    if track:
        requests.put(f'https://qa-scooter.praktikum-services.ru/api/v1/orders/cancel', json={'track': track})