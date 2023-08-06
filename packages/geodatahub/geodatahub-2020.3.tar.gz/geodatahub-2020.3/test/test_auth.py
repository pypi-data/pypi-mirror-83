#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pathlib
import json
import logging

import pytest

import geodatahub

@pytest.fixture
def auth(monkeypatch, tmp_path):
    """This is a fixture to generate a mock auth object"""
    # Test reading empty file from default file system location
    auth = geodatahub.auth.GeodatahubAuth()
    # Application of the monkeypatch to replace Path.home
    # with the behavior of mockreturn defined above.
    def fake_home():
        return tmp_path
    monkeypatch.setattr(pathlib.Path, "home", fake_home)
    yield auth

def test_init(auth):
    """Test the class can be initialized"""
    assert auth is not None


def test_login_settings(auth):
    """Test the class can be initialized"""
    assert auth is not None
    assert auth._redirect_url is not None
    assert auth._app_id is not None
    assert auth._base_url is not None
    assert auth.auth_url is not None


def test_loading_token_default(auth):
    """Test the class can locate an existing refresh token"""
    # No token set anywhere
    auth.refresh_token = None
    assert auth.get_stored_token() == None
    assert auth.refresh_token is None

def test_loading_token_class(auth, monkeypatch):
    # Test reading from class variable is prefered
    monkeypatch.setenv("GDH_REFRESH_TOKEN", "TestingToken")
    auth.refresh_token = "ClassToken"
    assert auth.get_stored_token() == "ClassToken"

def test_loading_token_envvars(auth, monkeypatch):
    # Test reading from env vars
    monkeypatch.setenv("GDH_REFRESH_TOKEN", "TestingToken")
    auth.refresh_token = None
    assert auth.get_stored_token() == "TestingToken"
    assert auth.refresh_token == "TestingToken"

def test_loading_token_filesystem(auth, tmp_path):
    # Test reading empty file from default file system location
    test_cases = [
        [os.path.join(tmp_path, ".gdh"),\
         None, \
         "TestingHomeFolderToken"],
        [os.path.join(tmp_path, ".custom"),\
         os.path.join(tmp_path, ".custom/authentication"),\
         "TestingCustomFolderToken"],
    ]

    for filepath, custom_folder, test_token in test_cases:
        # Reset class on every test
        auth.refresh_token = None

        # Ensure the file exists
        pathlib.Path(filepath).mkdir(parents=True)

        with open(os.path.join(filepath, "authentication"), 'w') as f:
            json.dump({}, f)
        assert auth.get_stored_token(custom_folder) is None
        assert auth.refresh_token is None

        # Store a test token in the file
        with open(os.path.join(filepath, "authentication"), 'w') as f:
            json.dump({"refresh_token":test_token}, f)
        assert auth.get_stored_token(custom_folder) == test_token
        assert auth.refresh_token == test_token

        # Reset class variable
        auth.refresh_token = None

        # Store multiple tokens in the file
        with open(os.path.join(filepath, "authentication"), 'w') as f:
            json.dump({"refresh_token":test_token+'2',
                       "access_token":"ACCESSTOKEN"}, f)
        assert auth.get_stored_token(custom_folder) == test_token+"2"
        assert auth.refresh_token == test_token+"2"


def test_storing_token_envvars(auth):
    # Test storing token in env vars
    auth.store_token(token = "TestingEnvvarToken",
                     location = "envvar")
    assert os.getenv("GDH_REFRESH_TOKEN") == "TestingEnvvarToken"

    # Test using class token
    auth.refresh_token = "TestingEnvvarClassToken"
    auth.store_token(location = "envvar")
    assert os.getenv("GDH_REFRESH_TOKEN") == "TestingEnvvarClassToken"

def test_storing_token_fs(auth):
    # Test storing token on disk
    auth.store_token(token = "TestingFsToken",
                     location = "disk")

    token_path = os.path.join(pathlib.Path.home(), ".gdh/authentication")
    with open(token_path) as f:
        auth_config = json.load(f)
        assert "TestingFsToken" == auth_config["refresh_token"]

def test_login(auth):
    """Given the user needs to login
       When they supply an invalid one-time code
       Then the login should fail and they should know why
    """
    with pytest.raises(RuntimeWarning):
        auth.login("NotAValidCode")
    assert auth.refresh_token == None
    assert auth.id_token == None
    assert auth.access_token == None

    """
    This test is disabled because the RuntimeError
    is raised on multiple errors

    # Test with something that has the correct format
    # but has been used
    with pytest.raises(RuntimeError):
        assert auth.login("5ee3aeb2-4fa8-4b4f-86ac-94d763ad5084")
    assert auth.refresh_token == None
    assert auth.id_token == None
    assert auth.access_token == None
    """
