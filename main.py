#!/usr/bin/env python3

import argparse
import keyring
import os
import requests
import subprocess
import sys
import tempfile
from getpass import getpass

class Chimpcom:
    def __init__(self) :
        self.action_id = None
        parser = argparse.ArgumentParser(description="Send Chimpcom command")
        parser.add_argument("--token", action=argparse.BooleanOptionalAction)
        parser.add_argument("--url", default="https://deviouschimp.co.uk/api/respond")
        parser.add_argument("--username", nargs="?")
        parser.add_argument("command", nargs="*")
        self.args = parser.parse_args()

        username = self.args.username

        if not username:
            username = input("Username: ")

        service_id = "chimpcom"+self.args.url
        token = keyring.get_password(service_id, username)

        if not token or self.args.token:
            token = getpass("Enter your token: ")

        if not token:
            print("No token.")
            sys.exit(1)

        keyring.set_password(service_id, username, token)

        # Single command
        if self.args.command:
            self.get_response(" ".join(self.args.command), token)
            sys.exit()

        # Interactive
        while True:
            cmd_in = input("> ")
            if cmd_in == "exit":
                sys.exit()
            self.get_response(cmd_in, token)

    def get_response(self, cmd_in, token):
        data = {
            "action_id": self.action_id,
            "cmd_in": cmd_in,
            "format": "cli"
        }

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        r = requests.post(self.args.url, headers=headers, json=data)

        res = r.json();
        self.action_id = res['action_id'];

        if r.status_code == 200:
            if res['edit_content']:
                tmp = tempfile.NamedTemporaryFile( mode = "w", delete=False )
                tmp.write( res['edit_content'] )
                tmp.close()

                subprocess.call( [ os.environ.get('EDITOR', '') or 'vi', tmp.name ] )

                tmp = open(tmp.name, 'r')
                updated_content = tmp.read()
                tmp.close()
                os.remove(tmp.name)

                self.save_content(updated_content, token)
            else:
                print(res['cmd_out'])
        else:
            print("Error " + str(r.status_code) + ". Invalid URL?")


    def save_content(self, content, token):
        data = {
            "action_id": self.action_id,
            "cmd_in": "",
            "content": content,
            "format": "cli"
        }

        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        print("Sending content...")

        r = requests.post(self.args.url, headers=headers, json=data)
        res = r.json()
        self.action_id = res['action_id']

        if r.status_code == 200:
            print(res['cmd_out'])
        else:
            print("Error " + str(r.status_code) + ". Invalid URL?")

cmd = Chimpcom()