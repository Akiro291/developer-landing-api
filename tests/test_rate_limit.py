import time
from fastapi import status

def test_rate_limit(client):
    contact_data = {
        "name": "Test User",
        "email": "test@example.com",
        "comment": "Это тестовое сообщение для проверки rate limit."
    }
    
    for i in range(5):
        response = client.post("/api/contact/", json=contact_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    response = client.post("/api/contact/", json=contact_data)
    
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "Rate limit exceeded" in response.json()["message"]
