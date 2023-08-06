# content of conftest.py
import os
import json

import pytest

from geodatahub.connection import Connection

# CONSTANTS
BASEURL = "https://vggdu1grc1.execute-api.eu-west-1.amazonaws.com/Dev"

def pytest_generate_tests(metafunc):
    """This function generates parameterized tests to run both real and mocked backends
    """
    if "connection" in metafunc.fixturenames:
        metafunc.parametrize("connection", ["mock_backend", "real_backend"], indirect=True)

mock_data_storage = {}

def fake_backend(*args, **kwargs):
    if "GET" in args or kwargs["method"] == "GET":
        if "datasets" in kwargs["path"]:
            # Get the requested UUID
            # The path is datasets/uuid
            path_elements = kwargs["path"].split('/')
            uuid = path_elements[-1]

            dataset = None
            try:
                dataset = mock_data_storage[uuid]
            except KeyError:
                pass
            return dataset

    return True

@pytest.fixture(scope="class")
def connection(request):
    if request.param == "mock_backend":
        conn = Connection(backend_url = BASEURL)
        conn._call_endpoint = fake_backend

        # Load in testing data
        global mock_data_storage
        with open("test/fixtures/test_backend_data_example.json", "r") as f:
            json_datasets = json.load(f)
            for dataset in json_datasets:
                identifier = dataset["identifier"]
                mock_data_storage[identifier] = dataset
        return conn
    elif request.param == "real_backend":
        conn = Connection(backend_url = BASEURL)
        # Warm up connection
        conn.set_token()
        return conn
    else:
        raise ValueError("invalid internal test config")
