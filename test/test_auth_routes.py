import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi import status


@pytest.fixture()
def test_client():
    return TestClient(app)

# def test_register_user(test_client):
#     new_user_data = {
#         "username": "shanzzzzz",
#         "email": "shanzzzz@gmail.com",
#         "password": "Abc1abc2",
#         "role": "customer"
#     }

#     existing_user = {"email" : "shan1111@gmail.caom"}
#     response = test_client.post("/register", json=existing_user)
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

#     response = test_client.post("/register", json=new_user_data)
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json() == {"message" : "User registered successfully"}

#     invalid_user = {"email" : "shan1111gmail.caom"}
#     response = test_client.post("/register", json=invalid_user)
#     assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY



def test_login_user(test_client):
    login_data = {"username": "sam@gmail.com", "password": "Abc1abc2abc3"}
    response = test_client.post("/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert "access_token" in response_data
    assert "token_type" in response_data

@pytest.fixture()
def auth_headers(test_client):
    login_data = {
        "username": "sam@gmail.com",
        "password": "Abc1abc2abc3"
    }
    response = test_client.post("/login", data=login_data)
    assert response.status_code == status.HTTP_200_OK
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# def test_get_user_profile(test_client, auth_headers):
#     response = test_client.get("/get_profile", headers=auth_headers)
#     assert response.status_code == status.HTTP_200_OK
#     assert "id" in response.json()
#     assert "username" in response.json()
#     assert "email" in response.json()
#     assert "role" in response.json()



# def test_get_all_user(test_client, auth_headers):
#     response = test_client.get("/get_all_user", headers=auth_headers)
#     assert response.status_code == status.HTTP_200_OK


def test_update_profile(test_client, auth_headers):
    data = {"is_active": True, "shop_owner_id": 22}
    response = test_client.put("/update_profile", headers=auth_headers, data=data)
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    # print(response_data)
    # assert "message" in response_data


# def test_change_user_password(test_client, auth_headers):
#     change_password_data = {
#         "old_password": "Abc1abc2abc3",
#         "new_password": "Abc1abc2abc4",
#     }
#     response = test_client.put("/change-password", data=change_password_data, headers=auth_headers)
#     assert response.status_code == status.HTTP_200_OK
#     response_data = response.json()
#     assert "message" in response_data


# def test_reset_password_mail(test_client):
#     reset_password_data = {"email": "sam@gmail.com"}
#     response = test_client.post("/reset-password-mail", data=reset_password_data)
#     assert response.status_code == status.HTTP_200_OK
#     response_data = response.json()
#     assert "message" in response_data