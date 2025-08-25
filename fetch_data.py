import requests
import pandas as pd

# Your API credentials
USER_ID = "8da99757-7c6e-467c-9024-6d254e6645e3"
API_TOKEN = "edfc9a0b-e1a4-46eb-9021-67e81dd438ac"

headers = {
    "x-api-user": USER_ID,
    "x-api-key": API_TOKEN
}

# Example: Fetch your habits
url = "https://habitica.com/api/v3/tasks/user"
response = requests.get(url, headers=headers)
data = response.json()["data"]  

# Convert to DataFrame for easier manipulation
df = pd.json_normalize(data)

# Optional: filter only habits
habits_df = df[df["type"] == "habit"]

# Save to CSV (prototype-ready!)
habits_df.to_csv("habitica_habits.csv", index=False)
print("Export done ✅")
