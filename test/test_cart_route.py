# from fastapi.testclient import TestClient
# from main import app

# client = TestClient(app)

# def test_add_item_to_cart():
#     item_data = {
#         "product_id": 1,
#         "quantity": 2
#     }
# response = client.post("/cart/", json=item_data)
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_get_cart_items():
#     response = client.get("/cart/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_update_cart_quantity():
#     updated_quantity_data = {
#         "new_quantity": 3
#     }
#     response = client.put("/cart/1", json=updated_quantity_data)
#     assert response.status_code == 200
#     assert response.json()["quantity"] == 3

# def test_remove_item_from_cart():
#     response = client.delete("/cart/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1
