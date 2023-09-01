#!/usr/bin/env python3

import argparse
import keyring
import os
import requests
import subprocess
import sys
import tempfile
from cmd import Cmd
from getpass import getpass


class Chimpcom(Cmd):
    intro = "Hello!\n"
    prompt = "> "
    username = ""
    file = None
    action_id = None
    args = None
    token = None

    def __init__(self, completekey="tab", stdin=None, stdout=None):
        super().__init__()

        parser = argparse.ArgumentParser(description="Send Chimpcom command")
        parser.add_argument("--token", action="store_true")
        parser.add_argument("--cleartoken", action="store_true")
        parser.add_argument("--url", default="https://deviouschimp.co.uk/api/respond")
        parser.add_argument("--username", nargs="?")
        parser.add_argument("command", nargs="*")
        self.args = parser.parse_args()
        self.username = self.args.username
        service_id = "chimpcom" + self.args.url

        if self.args.cleartoken:
            keyring.delete_password(service_id, self.username)
            print("Token cleared.")
            sys.exit()

        if not self.username:
            self.username = input("Username: ")

        self.token = keyring.get_password(service_id, self.username)

        if not self.token or self.args.token:
            self.token = getpass("Enter your token: ")

        if not self.token:
            print("No token.")
            sys.exit(1)

        keyring.set_password(service_id, self.username, self.token)

        # Single command
        if self.args.command:
            self.get_response(" ".join(self.args.command))
            sys.exit()

    def default(self, line):
        self.get_response(line)

    def get_response(self, cmd_in):
        r = self.make_request(
            {"action_id": self.action_id, "cmd_in": cmd_in, "format": "cli"}
        )

        res = r.json()

        if r.status_code == 200:
            self.action_id = res["action_id"]

            if res["edit_content"]:
                tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
                tmp.write(res["edit_content"])
                tmp.close()

                subprocess.call([os.environ.get("EDITOR", "") or "vi", tmp.name])

                tmp = open(tmp.name, "r")
                updated_content = tmp.read()
                tmp.close()
                os.remove(tmp.name)

                self.save_content(updated_content)
            else:
                print(res["cmd_out"])
        else:
            self.action_id = None
            print("Error " + str(r.status_code) + ". Invalid URL?")

    def save_content(self, content):
        params = {
            "action_id": self.action_id,
            "cmd_in": "",
            "content": content,
            "format": "cli",
        }

        print("Sending content...")

        r = self.make_request(params)
        res = r.json()
        self.action_id = res["action_id"]

        if r.status_code == 200:
            print(res["cmd_out"])
        else:
            print("Error " + str(r.status_code) + ". Invalid URL?")

    def make_request(self, json):
        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        return requests.post(self.args.url, headers=headers, json=json)

    def do_clear(self, args):
        print("Not implemented yet.")

    def do_quit(self, args):
        return self.do_exit(args)

    def do_exit(self, args):
        "Exit Chimpcom CLI"
        print("Bye!")
        return True


def parse(arg):
    return tuple(map(int, arg.split()))


if __name__ == "__main__":
    Chimpcom("tab", None, None).cmdloop()
