from fastapi import status

def test_create_contact_success(client):
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "comment": "Это тестовое сообщение для проверки работы API."
    }
    
    response = client.post("/api/contact/", json=contact_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == contact_data["name"]
    assert response.json()["email"] == contact_data["email"]
    assert "id" in response.json()

def test_create_contact_validation_error(client):
    contact_data = {
        "name": "",  # Пустое имя
        "email": "invalid-email",  # Невалидный email
        "comment": "Коротко"  # Слишком короткий комментарий
    }
    
    response = client.post("/api/contact/", json=contact_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "errors" in response.json()

def test_create_contact_missing_fields(client):
    contact_data = {
        "name": "Test User"
        # Отсутствуют email и comment
    }
    
    response = client.post("/api/contact/", json=contact_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_get_contact_not_found(client):
    response = client.get("/api/contact/99999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "Contact not found" in response.json()["detail"]
