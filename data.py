BASE_URL = 'https://qa-scooter.praktikum-services.ru'

ORDER_DATA = {
    "firstName": "Test",
    "lastName": "User",
    "address": "Test Address",
    "metroStation": 1,
    "phone": "+79998887766",
    "rentTime": 5,
    "deliveryDate": "2026-07-15",
    "comment": "Test order"
}

COLORS_DATA = [
    {"colors": ["BLACK"]},
    {"colors": ["GREY"]},
    {"colors": ["BLACK", "GREY"]},
    {"colors": []}
]

CREATE_COURIER_ENDPOINT = '/api/v1/courier'
LOGIN_COURIER_ENDPOINT = '/api/v1/courier/login'
DELETE_COURIER_ENDPOINT = '/api/v1/courier/{courier_id}'
CREATE_ORDER_ENDPOINT = '/api/v1/orders'
CANCEL_ORDER_ENDPOINT = '/api/v1/orders/cancel'
GET_ORDERS_ENDPOINT = '/api/v1/orders'