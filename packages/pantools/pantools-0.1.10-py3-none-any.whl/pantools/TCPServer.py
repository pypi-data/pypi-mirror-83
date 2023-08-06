import threading
import time,logging, sys, os
import socket
import pickle
from _thread import *
from pantools.net import announce_service, wait_for_announcement

from .logger import logger
from .send_recv import send_json, send_size, recv_size
from .ClientConnection import ClientConnection

# ================================================================
#
# ================================================================
class TCPServer:

    def __init__(self) -> None:
        self.clients = []
        self.subscribers = [] # deprecated
        self.msg_subscribers = {}
        self.ThreadCount = 0
        self.lock = threading.Lock()

    def print_clients(self, header) -> None:
        """Prints a table of active connections, followed by a table of active subscriptions"""
        logger.info("--- connection list {} ---".format(header))
        for c in self.connections:
            logger.info(c.getpeername())
        logger.info("--- end         ---")
        logger.info("--- subscriber list ---")
        for msgtype in self.msg_subscribers:
            logger.info("msgtype:{}".format(msgtype))
            for c in self.msg_subscribers[msgtype]:
                logger.info(c.getpeername())
        logger.info("--- end         ---")

    def setup_server(self, host, port, adv_magic=None, adv_port=None) -> None:
        """Creates a socket and starts listening. Also optionally starts an Anouncement thread"""
        self.ServerSocket = socket.socket()
        self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ThreadCount = 0
        try:
            logger.info("Binding to {}:{}".format(host, port))
            self.ServerSocket.bind((host, port))
        except socket.error as e:
            logger.info(str(e))
            sys.exit(1)

        logger.info("Listening for a Connection..")
        self.ServerSocket.listen(5)

        if adv_magic is not None and adv_port is not None:
            start_new_thread(self.advertise_service,(adv_magic, adv_port, host, port))

    def advertise_service(self, adv_magic, adv_port, service_host, service_port) -> None:
        logger.info("Starting an advertising thread {} on port {}. Service on {} {}".format(adv_magic, adv_port, service_host, service_port))
        while True:
            announce_service(adv_magic, adv_port, service_host, service_port)
            time.sleep(5)

    def add_client(self, client: ClientConnection) -> None:
        logger.info("Adding connection {}".format(client))
        self.lock.acquire()
        self.clients.append(client)
        self.lock.release()

        self.print_connections("After ADD")

    def remove_client(self, client) -> None:
        logger.info("Removing connection {}".format(client))

        self.lock.acquire()
        self.clients.remove(client)
        for msgtype in self.msg_subscribers:
            if client in self.msg_subscribers[msgtype]:
                print("Removing subscriber {}".format(client))
                self.msg_subscribers[msgtype].remove(client)
        self.lock.release()

        self.print_clients("After REMOVE")


    def add_subscriber(self, msgtype, client) -> None:
        logger.info("Adding subscriber {} {}".format(msgtype, client))
        self.lock.acquire()
        if msgtype not in self.msg_subscribers:
            self.msg_subscribers[msgtype] = []
        self.msg_subscribers[msgtype].append(client)
        self.lock.release()
        self.print_clients("After ADD SUB")

    def remove_subscriber(self, msgtype, client) -> None:
        logger.info("Removing subscriber {} {}".format(msgtype, client))
        self.lock.acquire()
        if msgtype not in self.msg_subscribers:
            self.lock.release()
            return
        self.msg_subscribers[msgtype].remove(client)
        self.lock.release()
        self.print_clients("After REMOVE SUB")

    def send_message_to_all_clients(self, msg) -> None:
        pass

    def send_message_to_subscribers(self, msg) -> None:
        self.lock.acquire()
        logger.debug("finding subscribers of msgtype {}".format(msgtype))
        if msg["msgtype"] in self.msg_subscribers:
            for c in self.msg_subscribers[msg["msgtype"]]:
                # Avoid sending message to ourselves
                # if c is not connection:
                logger.debug("Sending message to {}".format(c))
                send_json(c, msg)
                # else:
                #     logger.info("Skipping sending image to camera client!")

        self.lock.release()

    def accept_clients(self):
        while True:
            logger.debug("accept_clients() thread waiting...")
            client_socket, address = self.ServerSocket.accept()
            logger.info("Client connected: " + address[0] + ":" + str(address[1]))

            client = ClientConnection(client_socket, self)

            #self.add_connection(client_socket)
            self.add_client(client)

            self.print_clients("After CLIENT ACCEPTED")
            #start_new_thread(self.read_thread, (client_socket,))
            #self.ThreadCount += 1
            #logger.info("Started thread Number: " + str(self.ThreadCount))

    def stop_server(self):
        self.ServerSocket.close()
