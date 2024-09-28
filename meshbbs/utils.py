import logging
import time
import meshtastic
import meshtastic.stream_interface
import meshtastic.tcp_interface
import queue

from meshbbs import bbs

class MeshPacket:
    "This class represents the packet received from the sender"

    def __init__(self, packet, interface):
        self.interface = interface
        self.packet = packet
        self.message_bytes = None
        self.message_string = None
        self.sender_id = None
        self.to_id = None
        self.sender_node_id = None
        self.sender_short_name = None
        self.sender_long_name = None
        self.receiver_short_name = None

        try:
            if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
                self.message_bytes = packet['decoded']['payload']
                self.message_string = self.message_bytes.decode('utf-8')
                self.sender_id = packet['from']
                self.to_id = packet.get('to')
                self.sender_node_id = packet['fromId']

                self.sender_short_name = self.get_sender_short_name()
                self.sender_long_name = self.get_node_long_name()
                self.receiver_short_name = self.get_receiver_short_name() if self.to_id else "Group Chat"
                logging.info(f"Received message from user '{self.sender_short_name}' to {self.receiver_short_name}: {self.message_string}")
        except KeyError as e:
            logging.error(f"Error processing packet: {e}")

    def get_message(self) -> str:
        "return the message"
        return self.message_string
    
    def to_me(self) -> bool:
        "Return true if this packet is destined for me"

        if (self.to_id is not None and self.to_id != 0 and self.to_id != 255 and \
                self.to_id == self.interface.myInfo.my_node_num):
            return True
        else:
            return False

    def get_node_id_from_num(self, node_num) -> str:
        "Return the node ID"
        for node_id, node in self.interface.nodes.items():
            if node['num'] == node_num:
                return node_id
        return None

    def get_receiver_short_name(self) -> str:
        "Return the short name for the BBS"
        node_id = self.get_node_id_from_num(self.to_id)
        node_info = self.interface.nodes.get(node_id)
        if node_info:
            return node_info['user']['shortName']
        return None
    
    def get_sender_short_name(self) -> str:
        "Return the short name for the user"
        node_id = self.sender_node_id
        node_info = self.interface.nodes.get(node_id)
        if node_info:
            return node_info['user']['shortName']
        return None

    def get_node_long_name(self) -> str:
        "Return the long name for the user"
        node_id = self.sender_node_id
        node_info = self.interface.nodes.get(node_id)
        if node_info:
            return node_info['user']['longName']
        return None

def send_messages(send_q: queue.Queue, interface: meshtastic.stream_interface.StreamInterface) -> None:
    "The function we call as a thread to look for new messages and send them"
    max_payload_size = 200

    while True:
        (destination, message) = send_q.get()
        for i in range(0, len(message), max_payload_size):
            chunk = message[i:i + max_payload_size]
            try:
                d = interface.sendText(
                    text=chunk,
                    destinationId=destination,
                    wantAck=False,
                    wantResponse=False
                )
                logging.info(f"REPLY SEND ID={d.id}")
            except Exception as e:
                logging.info(f"REPLY SEND ERROR {e.message}")
        time.sleep(2)
        send_q.task_done()