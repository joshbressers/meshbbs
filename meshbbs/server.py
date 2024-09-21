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
import pubsub

# General logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def on_receive(packet, interface):
    try:
        if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
            message_bytes = packet['decoded']['payload']
            message_string = message_bytes.decode('utf-8')
            sender_id = packet['from']
            to_id = packet.get('to')
            sender_node_id = packet['fromId']

            sender_short_name = utils.get_node_short_name(sender_node_id, interface)
            receiver_short_name = utils.get_node_short_name(utils.get_node_id_from_num(to_id, interface),
                                                      interface) if to_id else "Group Chat"
            logging.info(f"Received message from user '{sender_short_name}' to {receiver_short_name}: {message_string}")

            if to_id is not None and to_id != 0 and to_id != 255 and to_id == interface.myInfo.my_node_num:
                process_message(sender_id, message_string, interface, is_sync_message=False)
            else:
                logging.info("Ignoring message sent to group chat or from unknown node")
    except KeyError as e:
        logging.error(f"Error processing packet: {e}")

def process_message(sender_id, message, interface, is_sync_message=False):
    utils.send_message(message, sender_id, interface)

def main():
    system_config = config_init.initialize_config()

    interface = config_init.get_interface(system_config)

    logging.info(f"TC²-BBS is running on {system_config['interface_type']} interface...")


    def receive_packet(packet, interface):
        on_receive(packet, interface)

    pubsub.pub.subscribe(receive_packet, system_config['mqtt_topic'])

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("Shutting down the server...")
        interface.close()

if __name__ == "__main__":
    main()
