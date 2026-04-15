from sheets import read_pending_rows, update_status, update_compliance_flag
from validation import validate_row
from compliance import classify_message
from scheduler import schedule_message, start_scheduler


def process_rows():
    """
    Read rows from sheet and process them through
    validation → compliance → scheduling
    """

    rows = read_pending_rows()

    print(f"\nTotal rows to process: {len(rows)}\n")

    for row in rows:

        row_number = row["sheet_row"]

        name = row["Name"]
        mobile = row["Mobile"]
        message = row["Message"]

        print(f"Processing row {row_number} for {name}")

        # -------------------------
        # STEP 1: VALIDATION
        # -------------------------

        valid, reason = validate_row(row)

        if not valid:
            print("Validation failed:", reason)

            update_status(row_number, "Invalid")

            continue

        # -------------------------
        # STEP 2: COMPLIANCE CHECK
        # -------------------------

        compliance_result = classify_message(message)

        print("Compliance result:", compliance_result)

        update_compliance_flag(row_number, compliance_result)

        if compliance_result != "Approved":

            update_status(row_number, "Blocked")

            print("Message blocked due to compliance\n")

            continue

        # -------------------------
        # STEP 3: SCHEDULE MESSAGE
        # -------------------------

        schedule_message(row)

        update_status(row_number, "Scheduled")

        print("Message scheduled\n")


def main():
    """
    Main workflow runner
    """

    print("\nStarting AI Investment Communication Workflow...\n")

    # process rows
    process_rows()

    # start scheduler
    start_scheduler()

    # keep program alive
    import time
    from scheduler import scheduler

    while True:
        jobs = scheduler.get_jobs()

        if len(jobs) == 0:
            print("All scheduled jobs completed. Shutting down scheduler.")
            scheduler.shutdown()
            break

        time.sleep(1)


if __name__ == "__main__":
    main()