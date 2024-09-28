#!/usr/bin/env python3

"""
meshbbs

This is where the main function exists, everything starts here
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
    "Start the whole thing"

    # The configuration data
    system_config = config_init.initialize_config()

    # The interface is the thing we use to communicate with the meshtastic node
    interface = config_init.get_interface(system_config)

    # Variables for holding data we'll use later
    send_q = queue.Queue()
    users = {}

    logging.info(f"meshbbs is running on {system_config['interface_type']} interface...")

    def receive_packet(packet, interface) -> None:
        "This function is run on ever message that is received"

        the_packet = utils.MeshPacket(packet, interface)
        if the_packet.to_me() == True:
            # Ignore packets not to us

            if the_packet.sender_id not in users:
                # Create a new user object if one doesn't exist
                # We should add some sort of timeout to these objects eventually
                # We probably have enough RAM on any machine to hold a lot of these
                users[the_packet.sender_id] = bbs.User(the_packet.get_node_long_name(), the_packet.get_receiver_short_name(), the_packet.sender_id, send_q)

            # When we receive a message, we call this function in the User object
            # to process what's happening
            users[the_packet.sender_id].parse(the_packet)

    # The meshtastic library uses a pubsub model for captuing messages
    # That sets this up to call receive_packet() when a message is received
    pubsub.pub.subscribe(receive_packet, system_config['mqtt_topic'])

    # Start a special thread for sending messages. If we want to send a message
    # We add it the send_q then this function picks it up and sends it
    sender = threading.Thread(target=utils.send_messages, args=[send_q, interface])
    sender.start()

    try:
        while True:
            # The main loop, everything happens in a thread
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
        interface.close()
        # It's very likely we should be doing more cleanup

if __name__ == "__main__":
    main()
