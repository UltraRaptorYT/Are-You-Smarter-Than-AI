from application.models import Entry
import datetime as datetime
import pytest
from flask import json

# Test Login API
# Validation Test
@pytest.mark.xfail(reason="Not Valid Username or Password")
@pytest.mark.parametrize("logInInfo", [
  ["sohhongyu@gmail.com","123", 0], # correct email and password
  ["sohhongyu123@gmail.com", "123", 1],  # Invalid credentials
  ["sohhongyu@gmail.com","123123", 1], # correct email but wrong password
  ["devops@gmail.com", "123", 1] # Invalid credentials
]
)
def test_loginAPI(client, logInInfo, capsys):
    with capsys.disabled():
        # prepare the data into a dictionary
        logInData = {
            "email": logInInfo[0],
            "password": logInInfo[1]
        }
    response = client.post('/api/login',
                           data=json.dumps(logInData),
                           content_type="application/json",)
    # check the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    response_body = json.loads(response.get_data(as_text=True))
    assert not response_body["isLogin"] == logInInfo[2]


# Test Sign Up API
# Validation Test
@pytest.mark.xfail(reason="User already exist")
@pytest.mark.parametrize("details", [
    ["DevOps", "devops@gmail.com", "123"], # New email
    ["Hong Yu", "sohhongyu@gmail.com", "123"],  # User already exist
]
)
def test_signUpAPI(client, details, capsys):
    with capsys.disabled():
          # prepare the data into a dictionary
          signUpData = {
              "username": details[0],
              "email": details[1],
              "password": details[2]
          }
          logInData = {
              "email": details[1],
              "password": details[2]
          }
    response = client.post('/api/signup',
                           data=json.dumps(signUpData),
                           content_type="application/json",)
    response_body = json.loads(response.get_data(as_text=True))
    # check the outcome of the action
    # assert response.status_code == 200
    # assert response.headers["Content-Type"] == "application/json"

    response = client.post('/api/login',
                           data=json.dumps(logInData),
                           content_type="application/json",)
    # check the outcome of the action
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    response = client.post(f'/user/delete/{response_body["id"]}',
                           content_type="application/json",)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"

