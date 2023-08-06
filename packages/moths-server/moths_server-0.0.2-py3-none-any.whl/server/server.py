import select
import json
import socket
import os
import time

from log.server_log_config import s_log as log
from log.server_log_config import log_deco

from metacls import ServerVerifier
from descriptors import PortVerifier

from db_interface import ServerDB as db

from common.settings import DEFAULT_PORT, \
    DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, MAX_PACKAGE_LENGTH, ENCODING

run = True


class Server(metaclass=ServerVerifier):

    port = PortVerifier()

    def __init__(self, addr=None, port=None):

        super().__init__()

        if addr is not None:
            self.addr = addr
        else:
            self.addr = DEFAULT_IP_ADDRESS
        if port is not None:
            self.port = port
        else:
            self.port = DEFAULT_PORT

        self.server_db = db()

        self.all_clients = []

        self.nicknames = {}

        self.wipe_queue = []

        self.run = False

        self.unlogged = []

    def read_requests(self, clients_to_read):

        responses = []

        for sock in clients_to_read:
            try:
                data = sock.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)

                data = self.response(data, sock)

                if isinstance(data, dict):
                    sock.send(json.dumps(data).encode(ENCODING))
                else:
                    responses.append(data)
            except Exception or socket.error:
                self.wipe_queue.append(sock)

        return responses

    def write_requests(self, cache, clients_to_write):

        for user in clients_to_write:
            if cache[user]:
                for messages in cache[user]:
                    for message in messages:

                        try:
                            c_list = self.server_db.fetch_contacts(
                                self.nicknames[user])

                            if c_list:
                                c_list = c_list.split(',')
                            else:
                                c_list = []
                        except Exception as e:
                            c_list = []
                            print(e)

                        try:
                            msg = json.dumps({"response": 101,
                                              "users": c_list,
                                              "to": message[0],
                                              "from": message[1][0],
                                              "message": message[1][1]})

                            self.server_db.add_contact(
                                username=self.nicknames[user],
                                other=message[1][0])

                            user.send(msg.encode(ENCODING))
                            cache[user].remove(message)
                        except Exception:
                            pass

    @log_deco
    def response(self, call, sock):

        try:
            call = json.loads(call)
        except Exception or socket.error:
            # log.error(e)  # LOG POINT
            pass

        if isinstance(call, dict):
            if call["action"] == "presence":
                try:
                    c_list = self.server_db.fetch_contacts(
                        self.nicknames[sock])
                    if c_list:
                        c_list = c_list.split(',')
                    else:
                        c_list = []

                except Exception as e:
                    c_list = []
                    print(e)

                return {"response": 200, "alert": "Status: OK",
                        "contacts": c_list}

            elif call["action"] == "message":
                return [call["receiver"],
                        [self.nicknames[sock], call["contents"]]]
            else:
                return {"response": 400, "alert": "Wrong call."}
        else:
            return {"response": 202, "alert": f"ECHO: {call}"}

    def server_authenticate(self, connection):

        connection.send(json.dumps({"time": time.time(),
                                    "user": "",
                                    "action": ""}).encode(ENCODING))
        log_batch = json.loads(
            connection.recv(MAX_PACKAGE_LENGTH).decode(ENCODING))

        user = log_batch["user"]

        salt = os.urandom(32)
        connection.send(salt)
        password = connection.recv(MAX_PACKAGE_LENGTH)

        try:
            if log_batch["action"] == "login":

                servsidehash = self.server_db.fetch_userhash(user)

                if servsidehash == password:

                    self.server_db.user_login(user,
                                              connection.getpeername()[0],
                                              connection.getpeername()[1])
                    self.nicknames[connection] = user
                    return True
                else:
                    return False
            elif log_batch["action"] == "register":

                self.server_db.user_register(user,
                                             password, log_batch["fullname"],
                                             log_batch["email"],
                                             connection.getpeername()[0],
                                             connection.getpeername()[1])
                self.nicknames[connection] = user
                return True
        except Exception as e:
            print(e)
            return False

    @log_deco
    def wipe_user(self, user):

        try:
            log.info(f"User {self.nicknames[user]} disconnected.")
            self.server_db.user_logout(self.nicknames[user])
            del self.nicknames[user]
            del self.message_cache[user]
            self.all_clients.remove(user)

        except Exception or socket.error as e:
            log.error(e)
            pass

    def mainloop(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            sock.bind((self.addr, self.port))
            sock.listen(MAX_CONNECTIONS)
            sock.settimeout(0.05)

            while self.run:
                try:
                    conn, addr = sock.accept()
                except OSError:
                    pass
                else:
                    log.info(f"User connected {addr}")

                    self.unlogged.append(conn)

                    # self.all_clients.append(conn)
                finally:
                    wait = 0
                    self.clients_to_read = []
                    self.clients_to_write = []
                    self.message_cache = {}
                try:
                    for client in self.unlogged:
                        if self.server_authenticate(client):
                            self.unlogged.remove(client)
                            self.all_clients.append(client)

                            try:
                                c_list = self.server_db.fetch_contacts(
                                    self.nicknames[client])
                                if c_list:
                                    c_list = c_list.split(',')
                                else:
                                    c_list = []

                            except Exception as e:
                                c_list = []
                                print(e)

                            client.send(
                                json.dumps({"response": 102,
                                            "contacts": c_list,
                                            "alert": "Login successful!"}
                                           ).encode(ENCODING))
                        else:
                            print(f"{client} authentication failed!")
                    self.clients_to_read, self.clients_to_write, errors = \
                        select.select(self.all_clients,
                                      self.all_clients, [], wait)

                except Exception:
                    pass

                self.recieved_batch = self.read_requests(self.clients_to_read)

                for user in self.all_clients:
                    if user not in self.message_cache:
                        self.message_cache[user] = []
                    if self.recieved_batch:
                        for message in self.recieved_batch:
                            if message[0] == self.nicknames[user] or \
                                    message[1][0] == self.nicknames[user] or \
                                    message[0] == "all":
                                self.message_cache[user].append(
                                    self.recieved_batch)

                if self.message_cache:
                    self.write_requests(self.message_cache,
                                        self.clients_to_write)

                for user in self.wipe_queue:
                    self.wipe_user(user)
                self.wipe_queue = []


# cust_port, cust_addr = None, None
#
# try:
#     if '-p' in sys.argv:
#         cust_port = int(sys.argv[sys.argv.index('-p') + 1])
# except:
#     # print('Incorrect port assigned. Using default.')
#     log.warning('Incorrect port assigned. Using default.')  # LOG POINT
#
# try:
#     if '-a' in sys.argv:
#         cust_addr = str(sys.argv[sys.argv.index('-a') + 1])
# except:
#     # print('Incorrect address assigned. Using default.')
#     log.warning('Incorrect address assigned. Using default.')  # LOG POINT


# s = Server(port=cust_port, addr=cust_addr)
# run = True

# s.mainloop()
