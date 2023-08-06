import socket
import re
import select
from _thread import start_new_thread
import json
import time
import random

from functools import wraps

from log.client_log_config import c_log as log
from log.client_log_config import log_deco

from metacls import ClientVerifier

from common.settings import DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    MAX_PACKAGE_LENGTH, ENCODING, MESSAGE_STANDARD


class login_required:

    def __init__(self):
        pass

    def __call__(self, func):

        @wraps(func)
        def decorated(*args, **kwargs):
            if args[0].gui_out.authenticated:
                res = func(*args, **kwargs)
                return res
            else:
                return None

        return decorated


class Client(metaclass=ClientVerifier):

    def __init__(self, server=None, port=None, username=None, password=None,
                 fullname=None, email=None, gui_out=None):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if server:
            self.server = server
        else:
            self.server = DEFAULT_IP_ADDRESS
        if port:
            self.port = port
        else:
            self.port = DEFAULT_PORT
        if username:
            self.account_name = username
        else:
            self.account_name = 'user' + str(random.randint(100, 999))

        self.gui_out = gui_out

        self.addr = (self.server, self.port)
        self.client.setblocking(False)
        self.isConnected = False
        self.pass_hash = password
        self.queue = []
        self.last_msg = None
        self.online = ""
        self.pending_message = False
        self.log_batch = None
        self.auth_action = None
        self.fullname = fullname
        self.email = email
        self.salt = None
        super().__init__()

        log.info('Client instance has been started successfully.')  # LOG POINT

    def connect(self):

        try:
            self.client.connect(self.addr)
            log.info(
                f'Connection to {self.server}:{self.port} established. '
                f'Running at {self.client.getsockname()}...')
            # LOG POINT

        except socket.error as e:
            log.warning(re.findall(r'(?<=]).*', str(e))[0][1:])  # LOG POINT
            self.isConnected = False

    def client_authenticate(self, connection):

        try:
            if self.log_batch is None:
                try:
                    self.log_batch = json.loads(
                        connection.recv(MAX_PACKAGE_LENGTH).decode(ENCODING))

                    self.log_batch["user"] = self.account_name
                    self.log_batch["action"] = self.auth_action
                    self.log_batch["fullname"] = self.fullname
                    self.log_batch["email"] = self.email
                    connection.send(json.dumps(
                        self.log_batch).encode(ENCODING))

                except Exception as e:
                    log.warning(e)
            if self.salt is None:
                self.salt = connection.recv(32)
                try:
                    connection.send(self.pass_hash)
                    self.log_batch = None
                    self.salt = None
                    self.pass_hash = None
                except Exception as e:
                    log.warning(e)
        except Exception as e:
            log.warning(f"Authentication failed! {e}")

    def read(self):
        while True:
            self.client.setblocking(True)

            ready = select.select([self.client], [], [], 0.1)
            if ready[0]:
                if not self.gui_out.authenticated:
                    self.client_authenticate(self.client)

                try:
                    data = self.client.recv(MAX_PACKAGE_LENGTH).decode()
                    data = json.loads(data)
                except Exception as e:
                    data = None
                    print(e)
            else:
                data = None
            self.client.setblocking(False)

            if data and "response" in data:
                if str(data["response"]) == '101':
                    self.cache_message(data["to"], data["from"],
                                       {"time": time.time(),
                                        "sender": data["from"],
                                        "message": data["message"]})
                    self.pending_message = True
                    self.online = data["users"]
                elif str(data["response"]) == '102':
                    print(data["alert"],
                          f"Your nickname is: {self.account_name}\n")

                    self.last_msg = time.time()
                    self.gui_out.authenticated = True
                    self.isConnected = True

    @log_deco
    def poke(self, silently=None):
        call = {}

        call["action"] = "presence"
        call["time"] = time.time()
        call["type"] = "status"
        call["user"] = {
            "account_name": self.account_name,
            "status": "Connected"
        }
        call["contents"] = ""

        try:
            if silently is None:
                log.info('Poking server... Establishing connection...')
                # LOG POINT

            self.send(data=(json.dumps(call)))
            feedback = json.loads(
                self.client.recv(MAX_PACKAGE_LENGTH).decode(ENCODING))

        except Exception or socket.error:
            feedback = None

        if feedback is None:
            self.isConnected = False
            return False
        else:
            return feedback

    def send(self, data=None):

        self.last_msg = time.time()

        if data:
            self.queue.append(data)

        for msg in self.queue:
            try:
                self.client.send(str(data).encode(ENCODING))
                self.queue.remove(msg)
            except socket.error:
                break

    @log_deco
    @login_required()
    def message(self, user, text=None):

        call = MESSAGE_STANDARD

        call["action"] = "message"
        call["time"] = time.time()
        call["receiver"] = user
        call["user"] = self.account_name

        if text:
            if self.isConnected:
                call["contents"] = text
                try:
                    self.send(data=json.dumps(call))
                except Exception or socket.error as e:
                    log.warning(e)

    @login_required()
    def contacts(self):
        return self.online

    @login_required()
    def load_chat(self, contact):
        try:
            with open("cache/chat_cache_%s.json" % self.account_name,
                      'r', encoding="utf-8") as read_data:
                data = json.load(read_data)
                if contact in data:
                    return data[contact]
                else:
                    return []
        except Exception:
            return []

    @login_required()
    def cache_message(self, receiver, sender, message):

        if sender == self.account_name:
            contact = receiver
        else:
            contact = sender

        try:
            with open("cache/chat_cache_%s.json" % self.account_name,
                      'r', encoding="utf-8") as read_data:
                data = json.load(read_data)
        except Exception:
            data = {}

        try:
            message_list = data[contact]
        except Exception:
            message_list = []

        message_list.append(message)
        data[contact] = message_list

        try:
            json.dump(data,
                      open("cache/chat_cache_%s.json" % self.account_name,
                           'w+', encoding='utf-8'),
                      indent=2,
                      ensure_ascii=True)
        except Exception as e:
            print(e)

    @log_deco
    @login_required()
    def presence(self):
        if self.last_msg is not None:
            if (time.time() - self.last_msg) > 5:

                if not self.isConnected:
                    feedback = self.poke(silently=True)
                    if not feedback:
                        feedback = None
                else:
                    feedback = self.poke(silently=True)
                    if not feedback:
                        # print(f"Can't reach the server...")
                        log.warning("Can't reach the server...")  # LOG POINT
                        feedback = None

                if isinstance(feedback, dict):
                    if not self.isConnected:
                        self.isConnected = True
                        log.info(
                            f'Connection to '
                            f'{self.server}:{self.port} established. '
                            f'Running at '
                            f'{self.client.getsockname()}...')  # LOG POINT

                    if str(feedback["response"])[0] == '1':
                        print(feedback)
                    elif str(feedback["response"])[0] == '2':
                        if str(feedback["response"]) == '200':
                            try:
                                self.online = feedback["contacts"]
                            except Exception as e:
                                log.warning(e)
                        else:
                            print(feedback["alert"])

    def mainloop(self):
        self.connect()
        start_new_thread(self.read, ())
        while True:
            start_new_thread(self.presence, ())
            if self.last_msg is None:
                time.sleep(0.5)
            else:
                time.sleep(5)

# try:
#     cust_username = None
#
#     if '-username' in sys.argv:
#         cust_username = str(sys.argv[sys.argv.index('-username') + 1])
#     else:
#         log.info('No username assigned. Using random.')
#
#     c = Client(username=cust_username)
#
#     c.mainloop()
#
# except Exception as e:
#     log.error(e)
#     # print('Incorrect port assigned. Using default.')
#     log.error('Failed to start client. Exiting.')  # LOG POINT
