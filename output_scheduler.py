from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from messaging import send_message
from sheets import update_status

# create scheduler
scheduler = BackgroundScheduler()


def schedule_message(row):
    """
    Schedule sending a message based on the row data.
    """

    schedule_str = row["Schedule"]
    mobile = row["Mobile"]
    message = row["Message"]
    row_number = row["sheet_row"]

    # convert string to datetime
    schedule_time = datetime.strptime(schedule_str, "%Y-%m-%d %H:%M")

    scheduler.add_job(
        send_and_update,
        'date',
        run_date=schedule_time,
        args=[mobile, message, row_number]
    )

    print(f"Message scheduled for {mobile} at {schedule_time}")


def send_and_update(mobile, message, row_number):
    """
    Send message and update sheet status.
    """

    success = send_message(mobile, message)

    if success:
        update_status(row_number, "Sent")
    else:
        update_status(row_number, "Failed")


def start_scheduler():
    """
    Start APScheduler.
    """

    scheduler.start()
    print("Scheduler started...")