#!/usr/bin/env python3
"""Integration test module
"""
import requests


def register_user(email: str, password: str) -> None:
    """Checks user registration
    """
    url = "http://127.0.0.1:5000/users"
    payload = {
        "email": email,
        "password": password
    }

    response = requests.post(url, data=payload)
    data = response.json()

    assert response.status_code == 200
    assert data == {"email": email, "message": "user created"}

    response = requests.post(url, data=payload)
    data = response.json()

    assert response.status_code == 400
    assert data == {"message": "email already registered"}

def log_in_wrong_password(email: str, password: str) -> None:
    """Login in with wrong password check
    """
    url = "http://127.0.0.1:5000/sessions"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload)

    assert response.status_code == 401

def log_in(email: str, password: str) -> str:
    """Login checks"""
    url = "http://127.0.0.1:5000/sessions"
    payload = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=payload) 
    data = response.json()

    assert response.status_code == 200
    assert data == {"email": email, "message": "logged in"}

    return response.cookies.get("session_id")

def profile_unlogged() -> None:
    """Profile check when not logged"""
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url)

    assert response.status_code == 403

def profile_logged(session_id: str) -> None:
    """Logged in profile check"""
    url = "http://127.0.0.1:5000/profile"
    response = requests.get(url, cookies={"session_id": session_id})

    data = response.json()

    assert response.status_code == 200

    assert data == {"email": EMAIL}

def log_out(session_id: str) -> None:
    """Logout checks"""
    url = "http://127.0.0.1:5000/sessions"
    response = requests.delete(url, cookies={"session_id": session_id})

    assert response.status_code == 200
    assert response.json() == {"message":"Bienvenue"}


def reset_password_token(email: str) -> str:
    """Password reset check"""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {
        "email": email
    }
    response = requests.post(url, data=payload)
    data = response.json()

    assert response.status_code == 200

    token = data.get("reset_token")

    assert data == {"email": email, "reset_token": token}

    return token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Reset password check"""
    url = "http://127.0.0.1:5000/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }

    response = requests.put(url, data=payload)
    data = response.json()

    assert response.status_code == 200

    assert data == {"email": email, "message": "Password updated"}

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
