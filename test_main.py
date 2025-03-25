# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data

def test_check_password_correct(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns valid when correct.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abcd1234!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password works"
    assert data.get("valid") is True

def test_check_password_short(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns invalid when short.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abcd12!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password too short"
    assert data.get("valid") is False

def test_check_password_no_digit(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns invalid when no digit is present.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abcd!efg"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password must contain at least one digit"
    assert data.get("valid") is False

def test_check_password_no_uppercase(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns invalid when no uppercase letter is present.
    """ 
    resp = client.post("/v1/checkPassword", json={"password": "abcd1234!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password must contain at least one uppercase letter"
    assert data.get("valid") is False

def test_check_password_no_special(client):
    """
    Test the POST '/v1/checkPassword' endpoint to ensure
    it returns invalid when no special character is present.
    """
    resp = client.post("/v1/checkPassword", json={"password": "Abcd1234"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("reason") == "Password must contain at least one special character"
    assert data.get("valid") is False