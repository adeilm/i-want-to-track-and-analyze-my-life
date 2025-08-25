import os
import csv
from dotenv import load_dotenv
from habitica_client import HabiticaClient

def process_and_save_tasks(tasks, task_type, filename):
    """
    Processes a list of tasks and saves them to a CSV file.

    Args:
        tasks (list): A list of task dictionaries.
        task_type (str): The type of task to process (e.g., 'habit', 'daily', 'todo').
        filename (str): The path to the output CSV file.
    """
    filtered_tasks = [task for task in tasks if task.get("type") == task_type]

    if not filtered_tasks:
        print(f"No tasks of type '{task_type}' found.")
        return

    # Define CSV headers based on common and type-specific fields
    headers = ['id', 'text', 'notes', 'priority', 'createdAt', 'updatedAt']
    if task_type == 'habit':
        headers.extend(['up', 'down', 'counterUp', 'counterDown'])
    elif task_type == 'daily':
        headers.extend(['streak', 'completed'])
    elif task_type == 'todo':
        headers.extend(['completed', 'date'])

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        for task in filtered_tasks:
            # Flatten nested 'challenge' if it exists
            if 'challenge' in task and isinstance(task.get('challenge'), dict):
                task.update({f"challenge_{k}": v for k, v in task['challenge'].items()})
            writer.writerow(task)

    print(f"Successfully saved {len(filtered_tasks)} {task_type}s to {filename}")

def main():
    """
    Main function to fetch data and save it to CSV files.
    """
    load_dotenv()

    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")
    HABITICA_API_TOKEN = os.getenv("HABITICA_API_TOKEN")

    if not HABITICA_USER_ID or not HABITICA_API_TOKEN:
        print("Error: HABITICA_USER_ID and HABITICA_API_TOKEN must be set in a .env file.")
        return

    client = HabiticaClient(HABITICA_USER_ID, HABITICA_API_TOKEN)
    tasks_data = client.get_tasks()

    if tasks_data and tasks_data.get("success"):
        tasks = tasks_data.get("data", [])

        # Create data directory if it doesn't exist
        if not os.path.exists('data'):
            os.makedirs('data')

        process_and_save_tasks(tasks, 'habit', 'data/habits.csv')
        process_and_save_tasks(tasks, 'daily', 'data/dailies.csv')
        process_and_save_tasks(tasks, 'todo', 'data/todos.csv')

        # We can also save rewards if needed
        # process_and_save_tasks(tasks, 'reward', 'data/rewards.csv')

    else:
        print("Failed to fetch tasks or request was not successful.")
        if tasks_data:
            print(tasks_data)

if __name__ == "__main__":
    main()
