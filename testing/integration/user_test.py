from requests import post, get
from integration_settings import BASE_URL
from data.user_test_data import CreateUserIN, GetUserOUT, CreateUserOUT
from util import resetDB, removeTimestamp


@resetDB
def test_create_user():
    validResponse = post(f"{BASE_URL}/user", json=CreateUserIN.validData1)
    noFieldResponse = post(f"{BASE_URL}/user", json=CreateUserIN.noField)
    invalidIDResponse = post(f"{BASE_URL}/user", json=CreateUserIN.invalidID)
    invalidPhoneResponse = post(f"{BASE_URL}/user", json=CreateUserIN.invalidPhone)
    repeatedResponse = post(f"{BASE_URL}/user", json=CreateUserIN.validData1)

    assert removeTimestamp(validResponse.json()) == CreateUserOUT.validData, \
        'Error en datos validos al crear usuario'
    assert removeTimestamp(noFieldResponse.json()) == CreateUserOUT.noField, \
        'Error en campo no enviado al crear usuario'
    assert removeTimestamp(invalidIDResponse.json()) == CreateUserOUT.invalidID, \
        'Error en cedula invalida al crear usuario'
    assert removeTimestamp(invalidPhoneResponse.json()) == CreateUserOUT.invalidPhone, \
        'Error en telefono invalido al crear usuario'
    assert removeTimestamp(repeatedResponse.json()) == CreateUserOUT.repeatedData, \
        'Error en usuario repetido al crear usuario'


@resetDB
def test_get_user():
    post(f"{BASE_URL}/user", json=CreateUserIN.validData1)

    validResponse = get(f"{BASE_URL}/user/1")
    invalidIDResponse = get(f"{BASE_URL}/user/a")
    notFoundResponse = get(f"{BASE_URL}/user/2")

    assert removeTimestamp(validResponse.json()) == GetUserOUT.responseUser, \
        'Error al validar data cuando se obtiene un usuario valido'
    assert removeTimestamp(invalidIDResponse.json()) == GetUserOUT.invalidID, \
        'Error en ID invalido al obtener usuario'
    assert removeTimestamp(notFoundResponse.json()) == GetUserOUT.noUser, \
        'Error en usuario no encontrado al obtener usuario'


@resetDB
def test_get_users():
    notFoundResponse = get(f"{BASE_URL}/users")
    assert removeTimestamp(notFoundResponse.json()) == GetUserOUT.noUsers, \
        'Error cuando no hay usuarios al obtener los usuarios'

    post(f"{BASE_URL}/user", json=CreateUserIN.validData1)
    post(f"{BASE_URL}/user", json=CreateUserIN.validData2)
    validResponse = get(f"{BASE_URL}/users")

    assert removeTimestamp(validResponse.json()) == GetUserOUT.responseUsers, \
        'Error al validar data cuando se obtienen los usuarios'
