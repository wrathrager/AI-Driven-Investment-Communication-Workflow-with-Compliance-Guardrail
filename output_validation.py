import re
from datetime import datetime

# Allowed categories from assignment
ALLOWED_CATEGORIES = [
    "Performance Update",
    "Research Insight",
    "Product Communication",
    "Marketing"
]


def validate_mobile(mobile):
    """
    Validate mobile number format.
    Accepts international format like +919876543210
    """
    if not mobile:
        return False

    mobile = str(mobile).strip()

    pattern = r'^\+?[1-9]\d{9,14}$'

    return bool(re.match(pattern, mobile))


def validate_message(message):
    """
    Ensure message is non-empty.
    """
    if message is None:
        return False

    message = str(message).strip()

    if message == "":
        return False

    return True


def validate_schedule(schedule):
    """
    Validate datetime format and ensure it is not in the past.
    Expected format: YYYY-MM-DD HH:MM
    """
    if not schedule:
        return False

    try:
        schedule_time = datetime.strptime(schedule, "%Y-%m-%d %H:%M")
    except ValueError:
        return False

    now = datetime.now()

    if schedule_time <= now:
        return False

    return True


def validate_category(category):
    """
    Validate category belongs to allowed list.
    """
    if not category:
        return False

    category = str(category).strip()

    return category in ALLOWED_CATEGORIES


def validate_row(row):
    """
    Validate an entire row from the sheet.

    Returns:
    (True, "Valid") if all checks pass
    (False, reason) if validation fails
    """

    mobile = row.get("Mobile")
    message = row.get("Message")
    schedule = row.get("Schedule")
    category = row.get("Category")

    if not validate_mobile(mobile):
        return False, "Invalid mobile number"

    if not validate_message(message):
        return False, "Empty message"

    if not validate_schedule(schedule):
        return False, "Invalid or past schedule"

    if not validate_category(category):
        return False, "Invalid category"

    return True, "Valid"