import pytest
import requests
from data import Urls, Endpoints, OrderData
from helpers import register_new_courier_and_return_login_password

@pytest.fixture
def create_courier():
    login_pass = register_new_courier_and_return_login_password()
    yield login_pass
    if login_pass:
        login, password = login_pass[0], login_pass[1]
        response = requests.post(f'{Urls.BASE_URL}{Endpoints.LOGIN_COURIER}', data={'login': login, 'password': password})
        if response.status_code == 200:
            courier_id = response.json().get('id')
            if courier_id:
                requests.delete(f'{Urls.BASE_URL}{Endpoints.DELETE_COURIER.format(courier_id=courier_id)}')


@pytest.fixture
def create_order():
    response = requests.post(f'{Urls.BASE_URL}{Endpoints.CREATE_ORDER}', json=OrderData.DEFAULT)
    track = response.json().get('track')
    yield ORDER_DATA, track
    if track:
        requests.put(f'{Urls.BASE_URL}{Endpoints.CANCEL_ORDER}', json={'track': track})