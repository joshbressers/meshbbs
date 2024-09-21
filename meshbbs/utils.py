import logging
import time
import meshtastic
import meshtastic.stream_interface
import meshtastic.tcp_interface

class MeshComms:
    def __init__(self, interface):
        self.interface: meshtastic.stream_interface.StreamInterface
        self.interface = interface

    def on_receive(self, packet) -> None:
        try:
            if 'decoded' in packet and packet['decoded']['portnum'] == 'TEXT_MESSAGE_APP':
                message_bytes = packet['decoded']['payload']
                message_string = message_bytes.decode('utf-8')
                sender_id = packet['from']
                to_id = packet.get('to')
                sender_node_id = packet['fromId']

                sender_short_name = self.get_node_short_name(sender_node_id)
                receiver_short_name = self.get_node_short_name(self.get_node_id_from_num(to_id)) if to_id else "Group Chat"
                logging.info(f"Received message from user '{sender_short_name}' to {receiver_short_name}: {message_string}")

                if to_id is not None and to_id != 0 and to_id != 255 and to_id == self.interface.myInfo.my_node_num:
                    self.process_message(sender_id, message_string)
                else:
                    logging.info("Ignoring message sent to group chat or from unknown node")
        except KeyError as e:
            logging.error(f"Error processing packet: {e}")

    def process_message(self, sender_id, message) -> None:
        self.send_message(message, sender_id)

    def send_message(self, message, destination) -> None:
        max_payload_size = 200
        for i in range(0, len(message), max_payload_size):
            chunk = message[i:i + max_payload_size]
            try:
                d = self.interface.sendText(
                    text=chunk,
                    destinationId=destination,
                    wantAck=False,
                    wantResponse=False
                )
                logging.info(f"REPLY SEND ID={d.id}")
            except Exception as e:
                logging.info(f"REPLY SEND ERROR {e.message}")

            
            time.sleep(2)

    def get_node_id_from_num(self, node_num) -> str:
        for node_id, node in self.interface.nodes.items():
            if node['num'] == node_num:
                return node_id
        return None


    def get_node_short_name(self, node_id) -> str:
        node_info = self.interface.nodes.get(node_id)
        if node_info:
            return node_info['user']['shortName']
        return None
