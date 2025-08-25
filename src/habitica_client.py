import os
import requests
from dotenv import load_dotenv

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
            response = requests.get(f"{self.base_url}/tasks/user", headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

if __name__ == "__main__":
    load_dotenv()

    HABITICA_USER_ID = os.getenv("HABITICA_USER_ID")
    HABITICA_API_TOKEN = os.getenv("HABITICA_API_TOKEN")

    if not HABITICA_USER_ID or not HABITICA_API_TOKEN:
        print("Error: HABITICA_USER_ID and HABITICA_API_TOKEN must be set in a .env file.")
    else:
        client = HabiticaClient(HABITICA_USER_ID, HABITICA_API_TOKEN)
        tasks_data = client.get_tasks()

        if tasks_data:
            print("Successfully fetched tasks:")
            # Print the number of tasks of each type
            if tasks_data.get("success"):
                tasks = tasks_data.get("data", [])
                habits = [task for task in tasks if task.get("type") == "habit"]
                dailies = [task for task in tasks if task.get("type") == "daily"]
                todos = [task for task in tasks if task.get("type") == "todo"]
                rewards = [task for task in tasks if task.get("type") == "reward"]
                print(f"  - Habits: {len(habits)}")
                print(f"  - Dailies: {len(dailies)}")
                print(f"  - Todos: {len(todos)}")
                print(f"  - Rewards: {len(rewards)}")
            else:
                print("Request was not successful.")
                print(tasks_data)
        else:
            print("Failed to fetch tasks.")
