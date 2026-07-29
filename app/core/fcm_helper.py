import os
import logging
import firebase_admin
from firebase_admin import credentials, messaging

logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK
_firebase_initialized = False

try:
    # Look for key in config directory, root directory, or environment variable
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    if not cred_path:
        # Default path
        cred_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "serviceAccountKey.json")
    
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        _firebase_initialized = True
        logger.info("Firebase Admin SDK initialized successfully.")
        print("Firebase Admin SDK initialized successfully.")
    else:
        logger.warning(f"Firebase service account key not found at: {cred_path}. Firebase functionality will be simulated.")
        print(f"WARNING: Firebase service account key not found at: {cred_path}. Push notifications will be simulated.")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
    print(f"ERROR: Failed to initialize Firebase Admin SDK: {e}")


def send_push_notification(token: str, title: str, body: str) -> bool:
    """
    Sends a push notification to a single device token.
    """
    if not token:
        logger.warning("FCM token is empty. Notification skipped.")
        return False

    if not _firebase_initialized:
        print(f"[SIMULATED PUSH] Sent to token ({token}): Title: '{title}' | Body: '{body}'")
        return True

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = messaging.send(message)
        logger.info(f"Successfully sent single message: {response}")
        print(f"FCM PUSH SENT SUCCESS: {response}")
        return True
    except Exception as e:
        logger.error(f"Error sending Firebase notification: {e}")
        print(f"FCM PUSH SENT ERROR: {e}")
        return False


def send_broadcast_notification(tokens: list[str], title: str, body: str) -> dict:
    """
    Sends a broadcast/multicast notification to a list of device tokens.
    """
    valid_tokens = [t for t in tokens if t and t.strip()]
    if not valid_tokens:
        logger.warning("No valid FCM tokens provided for broadcast.")
        return {"success_count": 0, "failure_count": 0, "status": "no_tokens"}

    if not _firebase_initialized:
        print(f"[SIMULATED BROADCAST] Sent to {len(valid_tokens)} devices: Title: '{title}' | Body: '{body}'")
        return {"success_count": len(valid_tokens), "failure_count": 0, "status": "simulated"}

    try:
        # Firebase send_multicast supports up to 500 tokens per call
        # Chunk them if necessary, but here we multicast simply
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=valid_tokens,
        )
        response = messaging.send_each_for_multicast(message)
        
        success_count = response.success_count
        failure_count = response.failure_count
        
        logger.info(f"Broadcast results: {success_count} success, {failure_count} failure.")
        print(f"FCM BROADCAST SENT: {success_count} succeeded, {failure_count} failed.")
        
        return {
            "success_count": success_count,
            "failure_count": failure_count,
            "status": "sent"
        }
    except Exception as e:
        logger.error(f"Error sending multicast notification: {e}")
        print(f"FCM BROADCAST ERROR: {e}")
        return {"success_count": 0, "failure_count": len(valid_tokens), "error": str(e), "status": "error"}


def send_topic_notification(topic: str, title: str, body: str) -> bool:
    """
    Sends a push notification to all devices subscribed to a topic.
    """
    if not _firebase_initialized:
        print(f"[SIMULATED TOPIC PUSH] Sent to topic '{topic}': Title: '{title}' | Body: '{body}'")
        return True

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            topic=topic,
        )
        response = messaging.send(message)
        logger.info(f"Successfully sent topic message: {response}")
        print(f"FCM TOPIC PUSH SENT SUCCESS: {response}")
        return True
    except Exception as e:
        logger.error(f"Error sending Firebase topic notification: {e}")
        print(f"FCM TOPIC PUSH SENT ERROR: {e}")
        return False
