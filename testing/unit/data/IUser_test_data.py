class IUserCases:
    validData = {
        "id": "1",
        "phone": "1234567890",
        "name": "Juan",
        "last_name": "Hernandez",
    }
    invalidID = {
        "id": "a",
        "phone": "1234567890",
        "name": "Juan",
        "last_name": "Hernandez",
    }
    invalidPhone = {
        "id": "1",
        "phone": "123",
        "name": "Juan",
        "last_name": "Hernandez",
    }
    invalidName = {
        "id": "1",
        "phone": "1234567890",
        "name": "Juan123",
        "last_name": "Hernandez",
    }
    invalidLastName = {
        "id": "1",
        "phone": "1234567890",
        "name": "Juan",
        "last_name": "Hernandez123",
    }
