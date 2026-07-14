import pytest
import requests
from helpers import register_new_courier_and_return_login_password
from data import BASE_URL, CREATE_ORDER_ENDPOINT, CANCEL_ORDER_ENDPOINT, ORDER_DATA, LOGIN_COURIER_ENDPOINT, DELETE_COURIER_ENDPOINT

@pytest.fixture
def create_courier():
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        login, password = login_pass[0], login_pass[1]
        response = requests.post(f'{BASE_URL}{LOGIN_COURIER_ENDPOINT}', 
                                 data={'login': login, 'password': password})
        if response.status_code == 200:
            courier_id = response.json().get('id')
            if courier_id:
                requests.delete(f'{BASE_URL}{DELETE_COURIER_ENDPOINT.format(courier_id=courier_id)}')


@pytest.fixture
def create_order():
    response = requests.post(f'{BASE_URL}{CREATE_ORDER_ENDPOINT}', json=ORDER_DATA)
    track = response.json().get('track')
    yield ORDER_DATA, track
    if track:
        requests.put(f'{BASE_URL}{CANCEL_ORDER_ENDPOINT}', json={'track': track})