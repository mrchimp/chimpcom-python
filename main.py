#!/usr/bin/env python3

import sys
import requests
import argparse
import keyring
from getpass import getpass


def get_response(cmd_in, token):
    data = {"cmd_in": cmd_in, "format": "cli"}
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        # TODO: would be better if we didn't need this...
        "X-Requested-With": "XMLHttpRequest",
    }

    r = requests.post(args.url, headers=headers, json=data)

    if r.status_code == 200:
        print(r.json()['cmd_out'])
    else:
        print("Network error. Invalid URL?")


username = input("Username: ")

parser = argparse.ArgumentParser(description="Send Chimpcom command")
parser.add_argument("command", nargs="?", help="command")
parser.add_argument("--url", default="https://deviouschimp.co.uk/api/respond")
args = parser.parse_args()
service_id = "chimpcom"+args.url
token = keyring.get_password(service_id, username)

if not token or args.command == "token":
    token = getpass("Enter your token: ")

if not token:
    print("No token.")
    sys.exit(1)

keyring.set_password(service_id, username, token)

while True:
    cmd_in = input("> ")
    if cmd_in == "exit":
        sys.exit()
    get_response(cmd_in, token)
