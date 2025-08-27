import os
import csv
import logging
import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class HabiticaClient:
    """
    A client for interacting with the Habitica API.
    """
    def __init__(self, user_id, api_token):
        """
        Initializes the HabiticaClient.

        Args:
            user_id (str): The user's Habitica ID.
            api_token (str): The user's Habitica API token.
        """
        self.base_url = "https://habitica.com/api/v3"
        self.headers = {
            "x-api-user": user_id,
            "x-api-key": api_token,
            "x-client": "i-want-to-track-and-analyze-my-life-app"
        }
        self.logger = logging.getLogger(__name__)
        
    def get_user(self):
        """
        Get user data from Habitica API
        """
        try:
            response = requests.get(f"{self.base_url}/user", headers=self.headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch user data: {e}")
            return None
    
    def get_tasks(self):
        """
        Fetches all tasks for the user.

        Returns:
            dict: A dictionary containing the user's tasks, or None if an error occurs.
        """
        try:
            response = requests.get(f"{self.base_url}/tasks/user", headers=self.headers, timeout=30)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Habitica get_tasks error: {e}")
            return None
if __name__ == "__main__":
    load_dotenv()

    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")
    HABITICA_API_TOKEN = os.getenv("HABITICA_API_TOKEN")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    if not HABITICA_USER_ID or not HABITICA_API_TOKEN:
        logger.error("HABITICA_USER_ID and HABITICA_API_TOKEN must be set in a .env file.")
    else:
        client = HabiticaClient(HABITICA_USER_ID, HABITICA_API_TOKEN)
        tasks_data = client.get_tasks()

        if tasks_data and tasks_data.get("success"):
            logger.info("Successfully fetched tasks:")
            tasks = tasks_data.get("data", [])
            habits = [task for task in tasks if task.get("type") == "habit"]
            dailies = [task for task in tasks if task.get("type") == "daily"]
            todos = [task for task in tasks if task.get("type") == "todo"]
            rewards = [task for task in tasks if task.get("type") == "reward"]
            logger.info(f"  - Habits: {len(habits)}")
            logger.info(f"  - Dailies: {len(dailies)}")
            logger.info(f"  - Todos: {len(todos)}")
            logger.info(f"  - Rewards: {len(rewards)}")
        else:
            logger.error("Failed to fetch tasks or request was not successful.")

def process_and_save_tasks(tasks, task_type, filename):
    """
    Processes a list of tasks and saves them to a CSV file.

    Args:
        tasks (list): A list of task dictionaries.
        task_type (str): The type of task to process (e.g., 'habit', 'daily', 'todo', 'reward').
        filename (str): The path to the output CSV file.
    """
    # Define CSV headers based on common and type-specific fields
    headers = ['id', 'text', 'notes', 'priority', 'createdAt', 'updatedAt', 'type']
    if task_type == 'habit':
        headers.extend(['up', 'down', 'counterUp', 'counterDown'])
    elif task_type == 'daily':
        headers.extend(['streak', 'completed'])
    elif task_type == 'todo':
        headers.extend(['completed', 'date'])

    count = 0
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers, extrasaction='ignore')
        writer.writeheader()
        for task in tasks:
            if task.get('type') != task_type:
                continue
            # Flatten nested 'challenge' if it exists
            if 'challenge' in task and isinstance(task.get('challenge'), dict):
                task.update({f"challenge_{k}": v for k, v in task['challenge'].items()})
            writer.writerow(task)
            count += 1

    if count == 0:
        logging.info(f"No tasks of type '{task_type}' found.")
    else:
        logging.info(f"Successfully saved {count} {task_type}(s) to {filename}")


logger = logging.getLogger(__name__)


def _flatten_dict(d, parent_key="", sep="."):
    """Flatten a nested dictionary using dot notation for keys."""
    items = {}
    for k, v in (d or {}).items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def process_and_save_user_stats(user_json, filename):
    """
    Extracts user stats from Habitica /user response and saves as a single-row CSV.

    Args:
        user_json (dict): The full response JSON from Habitica /user endpoint.
        filename (str): Output CSV path.
    """
    data = (user_json or {}).get("data", {})
    stats = data.get("stats", {})
    if not stats:
        logging.info("No user stats found in response.")
        return

    flat_stats = _flatten_dict(stats)
    headers = list(flat_stats.keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(flat_stats)
    logging.info(f"Saved user stats to {filename}")


def process_and_save_user_achievements(user_json, filename):
    """
    Extracts user achievements from Habitica /user response and saves as a single-row CSV.

    Args:
        user_json (dict): The full response JSON from Habitica /user endpoint.
        filename (str): Output CSV path.
    """
    data = (user_json or {}).get("data", {})
    achievements = data.get("achievements", {})
    if not achievements:
        logging.info("No user achievements found in response.")
        return

    flat_ach = _flatten_dict(achievements)
    headers = list(flat_ach.keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerow(flat_ach)
    logging.info(f"Saved user achievements to {filename}")

def main():
    """
    Main function to fetch data and save it to CSV files.
    """
    load_dotenv()

    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")
    HABITICA_API_TOKEN = os.getenv("HABITICA_API_TOKEN")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    if not HABITICA_USER_ID or not HABITICA_API_TOKEN:
        logging.error("HABITICA_USER_ID and HABITICA_API_TOKEN must be set in a .env file.")
        return

    client = HabiticaClient(HABITICA_USER_ID, HABITICA_API_TOKEN)

    # Fetch and save tasks
    tasks_data = client.get_tasks()
    if tasks_data and tasks_data.get("success"):
        tasks = tasks_data.get("data", [])

        # Create data directory if it doesn't exist
        data_dir = 'DataBase'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        process_and_save_tasks(tasks, 'habit', os.path.join(data_dir, 'habits.csv'))
        process_and_save_tasks(tasks, 'daily', os.path.join(data_dir, 'dailies.csv'))
        process_and_save_tasks(tasks, 'todo', os.path.join(data_dir, 'todos.csv'))
        process_and_save_tasks(tasks, 'reward', os.path.join(data_dir, 'rewards.csv'))
    else:
        logging.error("Failed to fetch tasks or request was not successful.")
        if tasks_data:
            logging.error(tasks_data)

    # Fetch and save user profile (stats and achievements)
    user_data = client.get_user()  # This should work now
    if user_data and user_data.get("success"):
        data_dir = 'DataBase'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        process_and_save_user_stats(user_data, os.path.join(data_dir, 'user_stats.csv'))
        process_and_save_user_achievements(user_data, os.path.join(data_dir, 'user_achievements.csv'))
    elif user_data is not None:
        logging.error("Failed to fetch user profile or request was not successful.")

if __name__ == "__main__":
    main()
