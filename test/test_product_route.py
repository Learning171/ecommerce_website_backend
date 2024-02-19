# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_create_new_product():
#     product_data = {
#         "name": "Test Product",
#         "description": "This is a test product.",
#         "price": 10.99,
#         "category": "Test Category"
#     }
# response = client.post("/products/", json=product_data)
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_read_all_products():
#     response = client.get("/products/")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_read_products_by_category():
#     response = client.get("/products/category/Test_Category")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_update_existing_product():
#     product_data = {
#         "name": "Updated Test Product",
#         "description": "This is an updated test product.",
#         "price": 15.99,
#         "category": "Updated Test Category"
#     }
#     response = client.put("/products/1", json=product_data)
#     assert response.status_code == 200
#     assert response.json()["name"] == "Updated Test Product"

# def test_delete_existing_product():
#     response = client.delete("/products/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1

# def test_upload_image():
#     files = {"file": ("test_image.jpg", open("test_image.jpg", "rb"), "image/jpeg")}
# response = client.post("/upload-image/?product_id=1", files=files)
#     assert response.status_code == 200
#     assert "image_id" in response.json()

# def test_update_image():
#     files = {"file": ("updated_test_image.jpg", open("updated_test_image.jpg", "rb"), "image/jpeg")}
#     response = client.put("/update-image/1", files=files)
#     assert response.status_code == 200
#     assert "image_id" in response.json()
