from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, timedelta
import subprocess
import os

def run_my_program():
    # Run the program
    program_path = os.path.join(os.path.dirname(__file__), 'argenprop/argenprop.py')
    subprocess.run(["python", program_path], check=True)
    # Update the last run time
    with open("last_run_time.txt", "w") as file:
        file.write(datetime.now().isoformat())

def run_additional_programs():
    # Run cleaning.py
    cleaning_program_path = os.path.join(os.path.dirname(__file__), 'cleaning.py')
    subprocess.run(["python", cleaning_program_path], check=True)

    # Run alerts.py
    alerts_program_path = os.path.join(os.path.dirname(__file__), 'alerts.py')
    subprocess.run(["python", alerts_program_path], check=True)

def missed_execution():
    try:
        with open("last_run_time.txt", "r") as file:
            last_run_time = datetime.fromisoformat(file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, assume the task has never run
        return True

    # Check if the task was missed: if current time is past 11 AM of the day after last run
    next_run_time = (last_run_time + timedelta(days=1)).replace(hour=11, minute=0, second=0, microsecond=0)
    return datetime.now() >= next_run_time

# Check for missed execution and run immediately if needed
if missed_execution():
    run_my_program()
    run_additional_programs()

# Set up the scheduler to run the task every day at 11 AM
scheduler = BlockingScheduler()
scheduler.add_job(run_my_program, 'cron', hour=11, minute=0)
scheduler.start()
