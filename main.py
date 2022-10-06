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
        print("Error " + str(r.status_code) + ". Invalid URL?")


parser = argparse.ArgumentParser(description="Send Chimpcom command")
parser.add_argument("--token", action=argparse.BooleanOptionalAction)
parser.add_argument("--url", default="https://deviouschimp.co.uk/api/respond")
parser.add_argument("--username", nargs="?")
parser.add_argument("command", nargs="*")
args = parser.parse_args()

username = args.username

if not username:
    username = input("Username: ")

service_id = "chimpcom"+args.url
token = keyring.get_password(service_id, username)

if not token or args.token:
    token = getpass("Enter your token: ")

if not token:
    print("No token.")
    sys.exit(1)

keyring.set_password(service_id, username, token)

# Single command
if args.command:
    get_response(" ".join(args.command), token)
    sys.exit()

# Interactive
while True:
    cmd_in = input("> ")
    if cmd_in == "exit":
        sys.exit()
    get_response(cmd_in, token)
