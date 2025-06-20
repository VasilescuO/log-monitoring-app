import csv
from datetime import datetime
from log_parser.app_logger import get_logger


def parse_log_file(filepath: str) -> dict:
    """
    Parses the log file and returns a dictionary with PID as key,
    and a dict containing start time, end time, and task description as values.

    Args:
        filepath (str): Path to the log file.
    Returns:
        dict: A dictionary where keys are PIDs and values are dictionaries with task details.
    """

    tasks_dict = {}
    with open(filepath, newline='') as log_file:
        reader = csv.reader(log_file)
        for line in reader:
            try:
                # define variables with task values
                task_timestamp = line[0].strip()
                task_name = line[1].strip()
                task_action = line[2].strip()
                task_pid = line[3].strip()
                # Convert timestamp string to a datetime object
                timestamp = datetime.strptime(task_timestamp, "%H:%M:%S")

                # create the PID entry if it doesn't exist
                try:
                    task_entry = tasks_dict[task_pid]
                except KeyError:
                    task_entry = {
                        "description": task_name,
                        "start": None,
                        "end": None
                    }
                    tasks_dict[task_pid] = task_entry

                # Assign timestamp based on action
                if task_action == "START":
                    task_entry["start"] = timestamp
                elif task_action == "END":
                    task_entry["end"] = timestamp

            except Exception as e:
                print(f"Failed to parse line: {line} -> {e}")
    return tasks_dict


def evaluate_durations(tasks_dict: dict) -> list:
    """
    Evaluates durations of jobs or completion and returns two list of status messages

    Args:
        tasks_dict (dict): Dictionary with PID as key and a dict containing start time, end time, and task description as values.
    Returns:
        list: A list of status messages indicating errors or warnings for tasks that took too long.
        list: A list of incomplete tasks that are missing either START or END timestamps.
    """
    output = []
    incomplete_tasks = []

    # Iterate through the task dictionary to calculate durations
    for pid, data in tasks_dict.items():
        start = data['start']
        end = data['end']
        description = data['description']

        # check if start or end are missing
        if not start or not end:
            incomplete_tasks.append(f"ERROR: PID {pid} ({description}): Incomplete log (missing START or END)")
            # write info log regarding incomplete tasks
            get_logger().info(f"{pid} ({description}): Incomplete log (missing START or END)")
            continue

        total_seconds = int((end - start).total_seconds())
        duration_minutes, duration_seconds = divmod(total_seconds, 60)

        if duration_minutes >= 10:
            output.append(f"ERROR: PID {pid} ({description}) took {duration_minutes} minutes and {duration_seconds} seconds")
            get_logger().error(f"{pid} ({description}) took {duration_minutes} minutes and {duration_seconds} seconds")
        elif duration_minutes >= 5:
            output.append(f"WARNING: PID {pid} ({description}) took {duration_minutes} minutes and {duration_seconds} seconds")
            get_logger().warning(f"{pid} ({description}) took {duration_minutes} minutes and {duration_seconds} seconds")
    return output, incomplete_tasks
