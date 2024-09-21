import logging
import time


def send_message(message, destination, interface) -> None:
    max_payload_size = 200
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

def get_node_id_from_num(node_num, interface) -> str:
    for node_id, node in interface.nodes.items():
        if node['num'] == node_num:
            return node_id
    return None


def get_node_short_name(node_id, interface) -> str:
    node_info = interface.nodes.get(node_id)
    if node_info:
        return node_info['user']['shortName']
    return None
