# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_create_address():
#     address_data = {
#         "street": "123 Main St",
#         "city": "City",
#         "state": "State",
#         "zipcode": "12345"
#     }
# response = client.post("/addresses/", json=address_data)
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_read_address():
#     response = client.get("/addresses/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1

# def test_update_address():
#     updated_address_data = {
#         "street": "456 Elm St",
#         "city": "Updated City",
#         "state": "Updated State",
#         "zipcode": "54321"
#     }
#     response = client.put("/addresses/1", json=updated_address_data)
#     assert response.status_code == 200
#     assert response.json()["street"] == "456 Elm St"

# def test_delete_address():
#     response = client.delete("/addresses/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1

# def test_list_addresses():
#     response = client.get("/addresses/")
#     assert response.status_code == 200
#     assert "items" in response.json()
#     assert "total" in response.json()
