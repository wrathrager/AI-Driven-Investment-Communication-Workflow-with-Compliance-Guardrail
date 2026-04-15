import time


def send_message(mobile, message):
    """
    Simulate sending a message.

    Returns True if sending is successful,
    False otherwise.
    """

    try:
        print("\n--- Sending Message ---")
        print("To:", mobile)
        print("Message:", message)

        # simulate network delay
        time.sleep(1)

        print("Message sent successfully\n")

        return True

    except Exception as e:
        print("Message sending failed:", e)

        return False