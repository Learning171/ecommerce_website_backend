# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_create_new_order():
#     order_data = {
#         "product_id": 1,
#         "quantity": 2
#     }
# response = client.post("/orders/", json=order_data)
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_read_order():
#     response = client.get("/orders/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1

# def test_read_orders():
#     response = client.get("/orders/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)
