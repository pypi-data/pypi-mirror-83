import threading
import time,logging, sys, os
import socket
import pickle
from _thread import *
from pantools.net import announce_service, wait_for_announcement

from .logger import logger
from .send_recv import send_json, send_size, recv_size

# ================================================================
#
# ================================================================
class TCPServer:

    def __init__(self) -> None:
        self.connections = []
        self.subscribers = [] # deprecated
        self.msg_subscribers = {}
        self.ThreadCount = 0
        self.lock = threading.Lock()

    def print_connections(self, header):
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

    def setup_server(self, host, port, adv_magic=None, adv_port=None):
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

    def advertise_service(self, adv_magic, adv_port, service_host, service_port):
        logger.info("Starting an advertising thread {} on port {}. Service on {} {}".format(adv_magic, adv_port, service_host, service_port))
        while True:
            announce_service(adv_magic, adv_port, service_host, service_port)
            time.sleep(5)

    def add_connection(self, connection):
        logger.info("Adding connection {}".format(connection))
        self.lock.acquire()
        self.connections.append(connection)
        self.lock.release()

        self.print_connections("After ADD")

    def remove_connection(self, connection):
        logger.info("Removing connection {}".format(connection))

        self.lock.acquire()
        self.connections.remove(connection)
        for msgtype in self.msg_subscribers:
            if connection in self.msg_subscribers[msgtype]:
                print("Removing connection {}".format(connection))
                self.msg_subscribers[msgtype].remove(connection)
        self.lock.release()

        self.print_connections("After REMOVE")


    def add_subscriber(self, msgtype, connection):
        logger.info("Adding subscriber {} {}".format(msgtype, connection))
        self.lock.acquire()
        if msgtype not in self.msg_subscribers:
            self.msg_subscribers[msgtype] = []
        self.msg_subscribers[msgtype].append(connection)
        self.lock.release()
        self.print_connections("After ADD SUB")

    def remove_subscriber(self, msgtype, connection):
        logger.info("Removing subscriber {} {}".format(msgtype, connection))
        self.lock.acquire()
        if msgtype not in self.msg_subscribers:
            self.lock.release()
            return
        self.msg_subscribers[msgtype].remove(connection)
        self.lock.release()
        self.print_connections("After REMOVE SUB")

    #
    # Thread started for each connection!
    #
    def read_thread(self, connection):

        # print("Starting thread for socket {}".format(connection))
        srcaddr, srcport = connection.getpeername()

        # print("Startar recv_size() loop")
        while True:
            try:
                data = recv_size(connection)
                obj = pickle.loads(data)

                message = obj["message"]
                msgtype = obj["msgtype"]

                if message == "subscribe":
                    logger.info("Received SUBSCRIBE...")
                    self.add_subscriber(msgtype, connection)
                    self.print_connections("After SUBSCRIBE")

                if message == "unsubscribe":
                    logger.info("Received UNSUBSCRIBE...")
                    self.remove_subscriber(msgtype, connection)
                    self.print_connections("After UNSUBSCRIBE")

                if message == "image":
                    logger.debug("Received image {}".format(obj["frameno"]))
                    self.lock.acquire()
                    logger.debug("finding subscribers of msgtype {}".format(msgtype))

                    if msgtype in self.msg_subscribers:
                        for c in self.msg_subscribers[msgtype]:
                            # Avoid sending message to ourselves
                            # if c is not connection:
                            logger.debug("Sending message to {}".format(c))
                            send_json(c, obj)
                            # else:
                            #     logger.info("Skipping sending image to camera client!")

                    self.lock.release()

            except Exception as e:
                logger.error(str(e))
                logger.info("Apparently the client hung up! Closing connection!")
                self.remove_connection(connection)
                connection.close()
                return # close thread!


    def accept_clients(self):
        while True:
            logger.debug("accept_clients() thread waiting...")
            client_socket, address = self.ServerSocket.accept()
            logger.info("Client connected: " + address[0] + ":" + str(address[1]))
            self.add_connection(client_socket)
            self.print_connections("After CLIENT ACCEPTED")
            start_new_thread(self.read_thread, (client_socket,))
            self.ThreadCount += 1
            logger.info("Started thread Number: " + str(self.ThreadCount))

    def stop_server(self):
        self.ServerSocket.close()
