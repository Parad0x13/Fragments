import requests
import re
import json
from pprint import pprint

from fragments.user import User

# [TODO] See if server.HTTP_OK and stuff like that can be used instead
HTTP_OK          = 200
HTTP_BAD_REQUEST = 400
HTTP_FORBIDDEN   = 403
HTTP_NOT_FOUND   = 404

url_server = "http://127.0.0.1:7777"

def shutdownServer():
    url = url_server + f"/shutdown"
    response = requests.get(url)

    if response.status_code == HTTP_OK: return True
    else: return None

def queryUser(username):
    url = url_server + f"/userdata/{username}"
    response = requests.get(url)

    if response.status_code == HTTP_OK: return response.json()
    else: return None

def createUser(username):
    url = url_server + f"/addrecord/{username}"

    response = requests.post(url, json = {"name": username, "exp": 0})

    if response.status_code == HTTP_OK: return True
    else: return False

def handleCommand_user(data):
    user_commands = ["query", "create", "delete"]
    if len(data) == 0 or data[0] not in user_commands:
        print(f"user commands: {user_commands}")
        return

    if len(data) < 2:
        print("Enter a username")
        return

    command = data[0]
    username = data[1]

    if False: pass
    elif command == "query":
        userData = queryUser(username)
        print(userData)
    elif command == "create":
        userData = createUser(username)
    elif command == "delete":
        pass

while True:
    data = input("Enter Command: ")
    data = data.split()

    if len(data) == 0: continue
    elif data[0] == "user": handleCommand_user(data[1:])
    elif data[0] == "shutdown": shutdownServer(); break
    elif data[0] == "exit": break
    else: print("Command not understood, try again")
