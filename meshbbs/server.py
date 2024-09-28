#!/usr/bin/env python3

"""
TC²-BBS Server for Meshtastic by TheCommsChannel (TC²)
Date: 07/14/2024
Version: 0.1.6

Description:
The system allows for mail message handling, bulletin boards, and a channel
directory. It uses a configuration file for setup details and an SQLite3
database for data storage. Mail messages and bulletins are synced with
other BBS servers listed in the config.ini file.
"""

import logging
import time

from meshbbs import config_init
from meshbbs import utils
from meshbbs import bbs
import pubsub

import queue
import threading

# General logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def main() -> None:
    system_config = config_init.initialize_config()
    interface = config_init.get_interface(system_config)
    send_q = queue.Queue()
    users = {}

    logging.info(f"meshbbs is running on {system_config['interface_type']} interface...")

    def receive_packet(packet, interface) -> None:
        the_packet = utils.MeshPacket(packet, interface)
        if the_packet.to_me() == True:

            if the_packet.sender_id not in users:
                users[the_packet.sender_id] = bbs.User(the_packet.get_node_long_name(), the_packet.get_receiver_short_name(), the_packet.sender_id, send_q)

            users[the_packet.sender_id].parse(the_packet)

    pubsub.pub.subscribe(receive_packet, system_config['mqtt_topic'])

    sender = threading.Thread(target=utils.send_messages, args=[send_q, interface])
    sender.start()

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
        interface.close()

if __name__ == "__main__":
    main()
