from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_execute_function():
    # Test opening calculator
    response = client.post(
        "/api/v1/execute",
        json={"prompt": "Open calculator"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["function"] == "open_calculator"
    assert "code" in data
    assert data["status"] == "success"

    # Test getting CPU usage
    response = client.post(
        "/api/v1/execute",
        json={"prompt": "Show CPU usage"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["function"] == "get_cpu_usage"
    assert "code" in data
    assert data["status"] == "success"

    # Test invalid prompt
    response = client.post(
        "/api/v1/execute",
        json={"prompt": "Invalid function that doesn't exist"}
    )
    assert response.status_code == 404 