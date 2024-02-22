#!/usr/bin/env python3
"""End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """ Test register_user Function """
    user = requests.post("http://172.27.55.185:5000/users",
                         {"email": email, "password": password})
    data = user.json()
    if user.status_code == 200:
        assert data['email'] == email
        assert data['message'] == "user created"
    else:
        assert user.status_code == 400
        assert data['message'] == 'email already registered'


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test log_in_wrong_password Function """
    user = requests.post("http://172.27.55.185:5000/sessions",
                         {"email": email, "password": password})
    assert user.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test log_in Function """
    user = requests.post("http://172.27.55.185:5000/sessions",
                         {"email": email, "password": password})

    if user.status_code == 200:
        data = user.json()
        assert data['email'] == email
        assert data['message'] == "logged in"
        return (user.cookies.get("session_id"))
    else:
        assert user.status_code == 401


def profile_unlogged() -> None:
    """ Test profile_unlogged Function """
    user = requests.get("http://172.27.55.185:5000/profile")
    assert user.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test profile_logged Function """
    user = requests.get("http://172.27.55.185:5000/profile",
                        cookies={"session_id": session_id})
    if user.status_code == 200:
        data = user.json()
        assert isinstance(data['email'], str)
    else:
        assert user.status_code == 403


def log_out(session_id: str) -> None:
    """ Test log_out Function """
    url = "http://172.27.55.185:5000/sessions"
    cookies = {"session_id": session_id}
    user = requests.delete(url, cookies=cookies)

    if user.ok:
        data = user.json()
        assert data['message'] == "Bienvenue"
    else:
        assert user.status_code == 403


def reset_password_token(email: str) -> str:
    """ Test reset_password_token Function """
    user = requests.post("http://172.27.55.185:5000/reset_password",
                         {"email": email})

    if user.status_code == 200:
        data = user.json()
        assert data['email'] == email
        assert isinstance(data['reset_token'], str)
        return (data['reset_token'])
    else:
        assert user.status_code == 403


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test update_password Function """
    url = "http://172.27.55.185:5000/reset_password"
    data = {
         "email": email,
         "reset_token": reset_token,
         "new_password": new_password
    }
    user = requests.put(url, data)

    if user.status_code == 200:
        data = user.json()
        assert data['email'] == email
        assert data['message'] == "Password updated"
    else:
        assert user.status_code == 403


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
