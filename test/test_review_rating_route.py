# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)

# def test_create_new_review_for_product():
#     review_data = {
#         "product_id": 1,
#         "rating": 5,
#         "comment": "Great product!"
#     }
# response = client.post("/reviews/1", json=review_data)
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_read_all_reviews_for_product():
#     response = client.get("/reviews/1")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_read_review_for_product():
#     response = client.get("/reviews/1/1")
#     assert response.status_code == 200
#     assert response.json()["id"] == 1
