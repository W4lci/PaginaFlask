import pytest
from src.funciones import *


@pytest.mark.parametrize(
    "usuario, contrasenia, expected", [
        ("admin", "123456",[(1, 'admin', '123456')]),
        ("admi", "12345", False),
        ("admi", "12345", False)]
        )

def test_login(usuario, contrasenia, expected):
    assert login(usuario, contrasenia) == expected


def test_bd():
    assert connect(cr.bd_ip, cr.bd_usr, cr.bd_pwr, cr.bd_name) != False
