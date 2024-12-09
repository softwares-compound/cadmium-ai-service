from datetime import datetime

def validate_message(message: dict) -> dict:
    """
    Validate the structure of an incoming WebSocket message.
    """
    required_fields = {"protocol_version", "type", "message_id", "timestamp"}
    if not all(field in message for field in required_fields):
        return None
    return message

def build_ack_message(message_id, status):
    """
    Build an acknowledgment message for the WebSocket protocol.
    """
    return {
        "protocol_version": "1.0",
        "type": "ack",
        "message_id": message_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": {"status": status}
    }
