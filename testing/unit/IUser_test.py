from pytest import raises
from src.application.data.IUser import IUser
from data.IUser_test_data import IUserCases


def test_valid_input():
    account = IUser(**IUserCases.validData)
    assert account.id == IUserCases.validData["id"], \
        'Error al obtener ID de una validacion correcta'
    assert account.phone == IUserCases.validData["phone"], \
        'Error al obtener telefono de una validacion correcta'
    assert account.name == IUserCases.validData["name"], \
        'Error al obtener nombre de una validacion correcta'
    assert account.last_name == IUserCases.validData["last_name"], \
        'Error al obtener apellido de una validacion correcta'


def test_invalid_ID():
    with raises(ValueError) as excinfo:
        IUser(**IUserCases.invalidID)
    assert excinfo.value.errors()[0]['msg'] == \
        "Value error, La cedula no es valida", 'Error al validar ID invalido'


def test_invalid_phone():
    with raises(ValueError) as excinfo:
        IUser(**IUserCases.invalidPhone)
    assert excinfo.value.errors()[0]['msg'] == \
        "Value error, El telefono no es valido", 'Error al validar telefono invalido'


def test_invalid_name():
    with raises(ValueError) as excinfo:
        IUser(**IUserCases.invalidName)
    assert excinfo.value.errors()[0]['msg'] == \
        "Value error, El nombre o apellido no son validos", 'Error al validar nombre invalido'


def test_invalid_lastName():
    with raises(ValueError) as excinfo:
        IUser(**IUserCases.invalidLastName)
    assert excinfo.value.errors()[0]['msg'] == \
        "Value error, El nombre o apellido no son validos", 'Error al validar apellido invalido'
