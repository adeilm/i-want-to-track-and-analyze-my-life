import os
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
            logger.error(f"Habitica get_tasks error: {e}")
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
