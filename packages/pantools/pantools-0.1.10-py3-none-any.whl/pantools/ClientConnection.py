import threading
import time,logging, sys, os
import socket
import pickle
from _thread import *
from pantools.net import announce_service, wait_for_announcement

from .logger import logger
from .send_recv import send_json, send_size, recv_size
#from .TCPServer import TCPServer

class ClientConnection:
    """ server is a TCPServer """
    def __init__(self, sock: socket, server) -> None:
        self.sock = sock
        self.server = server
        start_new_thread(self.read_thread, ())

    #
    # Thread started for each connection!
    #
    def read_thread(self, connection, server):

        # print("Starting thread for socket {}".format(connection))
        srcaddr, srcport = connection.getpeername()

        # print("Startar recv_size() loop")
        while True:
            try:
                data = recv_size(connection)
                obj = pickle.loads(data)

                # message : ["image", "subscribe", "unsubscribe", "announce"]
                # msgtype : ["image", "admin", ""]
                message = obj["message"]
                msgtype = obj["msgtype"]

                if message == "subscribe":
                    logger.info("Received SUBSCRIBE...")
                    #self.lookup_client(connection)
                    server.add_subscriber(msgtype, connection)
                    server.print_connections("After SUBSCRIBE")

                if message == "unsubscribe":
                    logger.info("Received UNSUBSCRIBE...")
                    server.remove_subscriber(msgtype, connection)
                    server.print_connections("After UNSUBSCRIBE")

                if message == "image":
                    logger.debug("Received image {}".format(obj["frameno"]))

                    server.send_message_to_all_subscribers(obj)

            except Exception as e:
                logger.error(str(e))
                logger.info("Apparently the client hung up! Closing connection!")
                server.remove_connection(connection)
                connection.close()
                return # close thread!

