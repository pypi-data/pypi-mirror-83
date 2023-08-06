#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging as lg
import json

from geodatahub.auth import GeodatahubAuth
from geodatahub.connection import Connection as GeodatahubConn

# Setup logging module
lg.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=lg.DEBUG)
LOG = lg.getLogger("geodatahub")
LOG.setLevel(lg.INFO)

url = "https://api-dev.geodatahub.dk"


def login(args):
    try:
        auth = GeodatahubAuth()
        if args.use_refresh_token:
            args.print_all_tokens = True
            access, refresh, identity = auth.refresh_auth()
        else:
            print("Please login at www.geodatahub.dk/login and paste the one-time code below,")
            code = input("One-time code: ")
            access, refresh, identity = auth.login(code)
            auth.store_token(refresh)
    except Exception:
        LOG.info("The login was not successful.")
    else:
        if args.print_all_tokens:
            print("Access Token")
            print("-------------")
            print(access)
            print("\n\n")

            print("Refresh Token")
            print("-------------")
            print(refresh)
            print("\n\n")

            print("Identity Token")
            print("---------------")
            print(identity)
            print("\n\n")

        LOG.info("Login completed!")


def test_connection(args):
    conn = GeodatahubConn(backend_url=url)
    if conn.ping():
        LOG.info("Connection to Geodatahub works")
    else:
        LOG.info("An error occured while contacting Geodatahub")


def search(args):
    """Perform search of datasets in Geodatahub
    """
    conn = GeodatahubConn(backend_url=url)

    # Process the users input.
    # The user might type: key1=val1 key2=val2
    # This must be translated into an acceptable query string
    # { "key1":val1, "key2":val2 }
    query = ""
    try:
        if args.query != "":
            query = []
            for q in args.query:
                q2 = q.split('=')
                query.append(f'"{q2[0]}":"{q2[1]}"')
            query = "{%s}" % ",".join(query)
    except IndexError:
        # User supplied the request in JSON format
        query = json.loads(args.query[0])
        for k in query:
            if "http" not in k:
                # Ensure all keys have the full schema URI
                query[f"https://schema.geodatahub.dk/{k}.json"] = query.pop(k)

    datasets = conn.searchDataset(query)
    if datasets is None:
        LOG.info("No datasets exist")
    else:
        for dset in datasets:
            LOG.info(dset)

def get_data(args):
    """Perform a GET request for a specific dataset in Geodatahub
    """
    conn = GeodatahubConn(backend_url=url)
    conn._auth_headers["Authorization"] = "eyJraWQiOiJsQWdWTGM3SWZseDRwYkVHVUI0c3c4Ykg0R3VQTDRJb2NcL25JVFU1RWJVRT0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoibVo4YTdPRzdOYjlqOXhPZXVZT0hXZyIsInN1YiI6ImFhNTk0NjdlLTlhZWYtNDg1NC1hNzYyLTkyMGZlMjBhOTc0NyIsImF1ZCI6IjFtZGQzMGI1a2Jza3E1cms5YjNyZDk2Y3YyIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNTk0NzU5NjA2LCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuZXUtd2VzdC0xLmFtYXpvbmF3cy5jb21cL2V1LXdlc3QtMV8wVURHeFdqNmQiLCJjb2duaXRvOnVzZXJuYW1lIjoiYWE1OTQ2N2UtOWFlZi00ODU0LWE3NjItOTIwZmUyMGE5NzQ3IiwiZXhwIjoxNTk0NzYzMjA2LCJpYXQiOjE1OTQ3NTk2MDYsImVtYWlsIjoiY2hyaXN0aWFuQGdlb2RhdGFodWIuZGsifQ.NzoYMWnEXHeuv_nZAVC6THiUDSoNeMuYDMvivBV4crutEpDrwvNypU_8iGPN29veBaEC02UPTajyW44nFE2j62kF8Cc6kyolUxBiPbbtedAYzwEENcqcccZJeTKja-09Fxqs8hCzH668CLPNcPD7Z0-jjFHJRysYnz7u3DPRjQb4K0HPCkhtv3u0e-UH6o3qZeh1HqpT4RAA6FQ8KxlbLFGejpB1dL19n6zBwcS2aAcLn4tFdVbOIpbfohxaJmQWCiwnaTeIdhyVO28e9eoiCtiPm8R1zw-5X5D-NMrjLZjBdAwCDw8K8ydGadcxH_ms2pARfeGCSnOsfaTAaBARKQ"
    dataset = conn.getDataset(args.id)
    LOG.info(dataset)

def schema(args):
    """Perform a GET request for a specific dataset in Geodatahub
    """
    conn = GeodatahubConn(backend_url=url)
    dataset = conn.get_schema_options(args.schema, args.key)

def add_data(args):
    conn = GeodatahubConn(backend_url=url)
    print(args.files)
    try:
        for f in args.files:
            with open(f, "r") as json_file:
                dataset = json.load(json_file)
                dset_id = conn.uploadDataset(dataset)
                for ids in dset_id:
                    LOG.info(f"New dataset added with ID {ids}")

    except FileNotFoundError:
        LOG.error(f"Unable to open one or more of the files {args.files}")

# Setup commandline arguments
cli_parser = argparse.ArgumentParser(description="Commandline interface to GeoDataHub")
sub_parser = cli_parser.add_subparsers(help= "Type of operation")
cli_parser.add_argument("--config-path", help="Location of the user config file")

# Commandline arguments to login to backend
auth_parser = sub_parser.add_parser("login")
auth_parser.add_argument("--print-all-tokens", default=False, const=True, nargs='?', help="Print auth tokens to screen")
auth_parser.add_argument("--use-refresh-token", default=False, const=True, nargs='?', help="Use existing refresh token to login. Token will refresh any existing tokens but not require a full login.")
auth_parser.set_defaults(func=login)

# Commandline arguments to test connection to backend
test_parser = sub_parser.add_parser("test")
test_parser.set_defaults(func=test_connection)

# Commandline arguments to search/list datasets
search_parser = sub_parser.add_parser("list")
search_parser.add_argument("query", nargs='+', help="Values to search for", default="")
search_parser.set_defaults(func=search)

# Commandline arguments to add new datasets
add_parser = sub_parser.add_parser("add")
add_parser.add_argument("files", nargs='+', help="List of JSON files containing metadata to upload")
add_parser.set_defaults(func=add_data)

# Commandline arguments to get a specific datasets
get_parser = sub_parser.add_parser("get")
get_parser.add_argument("id", help="Unique dataset identifier")
get_parser.set_defaults(func=get_data)

# Commandline arguments to get a specific datasets
schema_options_parser = sub_parser.add_parser("schema")
schema_options_parser.add_argument("schema", help="Unique dataset identifier")
schema_options_parser.add_argument("key", help="Unique dataset identifier")
schema_options_parser.set_defaults(func=schema)


if __name__ == "__main__":
    args = cli_parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        cli_parser.print_help()
        sys.exit(1)
