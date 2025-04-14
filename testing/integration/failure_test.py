from requests import get, post
from integration_settings import BASE_URL


def test_invalid_method():
    response = post(f"{BASE_URL}/users")
    assert response.status_code == 405, 'Error en metodo invalido'


def test_invalid_url():
    response = get(f"{BASE_URL}/pagar")
    assert response.status_code == 404, 'Error en ruta invalida'
