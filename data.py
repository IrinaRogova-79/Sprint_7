class Urls:
    BASE_URL = 'https://qa-scooter.praktikum-services.ru'


class Endpoints:
    CREATE_COURIER = '/api/v1/courier'
    LOGIN_COURIER = '/api/v1/courier/login'
    DELETE_COURIER = '/api/v1/courier/{courier_id}'
    CREATE_ORDER = '/api/v1/orders'
    CANCEL_ORDER = '/api/v1/orders/cancel'
    GET_ORDERS = '/api/v1/orders'


class OrderData:
    DEFAULT = {
        "firstName": "Test",
        "lastName": "User",
        "address": "Test Address",
        "metroStation": 1,
        "phone": "+79998887766",
        "rentTime": 5,
        "deliveryDate": "2026-07-15",
        "comment": "Test order"
    }
    
    COLORS = [
        {"colors": ["BLACK"]},
        {"colors": ["GREY"]},
        {"colors": ["BLACK", "GREY"]},
        {"colors": []}
    ]


class ErrorMessages:
    DUPLICATE_LOGIN = "Этот логин уже используется"
    MISSING_DATA = "Недостаточно данных для создания учетной записи"
    MISSING_LOGIN_DATA = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"