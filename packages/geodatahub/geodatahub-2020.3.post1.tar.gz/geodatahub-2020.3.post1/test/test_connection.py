#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import unittest
import re

import pytest

#import geodatahub
from geodatahub.connection import Connection
from geodatahub.auth import GeodatahubAuth

BASEURL = "https://cq6nowxuf4.execute-api.eu-west-1.amazonaws.com/dev/"

@pytest.fixture(scope="class")
def load_test_datasets():
    with open("test/fixtures/geodata_testdata.json", "r") as f:
        test_data = json.load(f)
    return test_data
"""
Monkeypatched/mocked version of integration endpoints
"""
def mock_refresh_auth(*args, **kwargs):
    return "id_token", "refresh_token", "access_token"

"""
Helper functions
"""
def get_auth_conn():
    """Get an authenticated connected to the API

    This object is reused by all test in this suite
    """
    conn = Connection(backend_url = "https://api-dev.geodatahub.dk")
    # Make sure the connection is ready
    conn._auth.refresh_auth()
    return conn

"""
Tests
"""
def test_auth_headers(monkeypatch):
    """
    Test that the auth headers are added when creating the
    connection object.
    """
    monkeypatch.setenv("GDH_REFRESH_TOKEN", "TestingToken")
    # MonkeyPatch the call to get auth tokens
    monkeypatch.setattr(GeodatahubAuth, 'refresh_auth', mock_refresh_auth)
    conn = get_auth_conn()
    assert conn._auth_headers == {"Authorization": "id_token"}

#
# Test that run both as mock and integration tests
#
def test_ping(connection):
    assert connection.ping() is True

def test_get_dataset_by_id(connection, load_test_datasets):
    # Test a non-existing identifier
    identifier = "ae7948f3-16e3-4b95-a9ea-2fd36b99f479"
    backend_dataset = connection.getDataset(identifier)
    assert backend_dataset == None

    for dataset in load_test_datasets:
        backend_dataset = connection.getDataset(dataset["identifier"])
        # Compare all keys
        for key in dataset.keys():
            assert getattr(backend_dataset, key) == dataset[key]
