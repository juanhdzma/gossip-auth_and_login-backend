class CreateUserIN:
    validData1 = {
        "id": "1",
        "phone": "3187951218",
        "name": "Juan",
        "last_name": "Hernandez"
    }
    validData2 = {
        "id": "2",
        "phone": "1234567890",
        "name": "Daniel",
        "last_name": "Saavedra"
    }
    noField = {
        "phone": "3187951218",
        "name": "Juan",
        "last_name": "Hernandez"
    }
    invalidPhone = {
        "id": "1",
        "phone": "1",
        "name": "Juan",
        "last_name": "Hernandez"
    }
    invalidID = {
        "id": "abc",
        "phone": "3187951218",
        "name": "Juan",
        "last_name": "Hernandez"
    }


class CreateUserOUT:
    validData = {
        "is_error": False,
        "data": "Usuario agregado correctamente",
        "status_code": 201
    }
    repeatedData = {
        "is_error": True,
        "message": "El usuario ya existe en la base de datos",
        "status_code": 409
    }
    noField = {
        "is_error": True,
        "message": "Field required",
        "status_code": 400
    }
    invalidPhone = {
        "is_error": True,
        "message": "Value error, El telefono no es valido",
        "status_code": 400
    }
    invalidID = {
        "is_error": True,
        "message": "Value error, La cedula no es valida",
        "status_code": 400
    }


class GetUserOUT:
    responseUser = {
        "is_error": False,
        "data": {
            "id": "1",
            "phone": "3187951218",
            "name": "Juan",
            "last_name": "Hernandez"
        },
        "status_code": 200
    }
    responseUsers = {
        "is_error": False,
        "data": [
            {
                "id": "1",
                "phone": "3187951218",
                "name": "Juan",
                "last_name": "Hernandez"
            },
            {
                "id": "2",
                "phone": "1234567890",
                "name": "Daniel",
                "last_name": "Saavedra"
            }
        ],
        "status_code": 200
    }
    noUsers = {
        "is_error": True,
        "message": "No hay usuarios en la base de datos",
        "status_code": 404
    }
    noUser = {
        "is_error": True,
        "message": "El usuario no esta en la base de datos",
        "status_code": 404
    }
    invalidID = {
        "is_error": True,
        "message": "Id no valido",
        "status_code": 400
    }
