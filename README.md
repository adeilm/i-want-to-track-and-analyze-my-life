# i-want-to-track-and-analyze-my-life

Automates habit tracking by pulling data from Habitica API into CSV files, ready to be used with visualization tools like Power BI. This tool tracks your habits, dailies, and todos, making it easy to analyze streaks, trends, and completion rates.

## Features

- **Automated Data Fetching:** Pulls your latest data directly from the Habitica API.
- **Structured Storage:** Organizes your data into clear, easy-to-use CSV files (`habits.csv`, `dailies.csv`, `todos.csv`).
- **Ready for Visualization:** The CSV output is designed to be easily imported into tools like Power BI, Tableau, or Google Sheets for analysis.
- **Scalable:** A solid foundation for building more complex life-tracking dashboards.

## Getting Started

Follow these instructions to get your own copy of the project up and running.

### Prerequisites

- Python 3.6+
- A Habitica account

### Installation

1.  **Clone the repository (if you haven't already):**
    ```sh
    git clone https://github.com/your-username/i-want-to-track-and-analyze-my-life.git
    cd i-want-to-track-and-analyze-my-life
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1.  **Create a `.env` file** for your API credentials by copying the example file:
    ```sh
    cp .env.example .env
    ```

2.  **Find your Habitica credentials:**
    - Log in to your [Habitica](https://habitica.com) account.
    - Navigate to **Settings > API**.
    - Copy your **User ID** and **API Token**.

3.  **Add your credentials to the `.env` file:**
    Open the `.env` file and replace the placeholder text with your actual credentials:
    ```
    HABITICA_USER_ID=your_user_id_here
    HABITICA_API_TOKEN=your_api_token_here
    ```

### Usage

Run the main script to fetch your data and generate the CSV files:

```sh
python3 src/process_data.py
```

Your CSV files (`habits.csv`, `dailies.csv`, `todos.csv`) will be saved in the `data/` directory.

## Next Steps: Visualization

You can now use the generated CSV files to create dashboards and visualizations.

### Example with Power BI

1.  Open Power BI Desktop.
2.  Click **Get Data** and select **Text/CSV**.
3.  Navigate to the `data/` directory and select one of the CSV files (e.g., `dailies.csv`).
4.  Power BI will automatically detect the headers and data types. Click **Load**.
5.  Repeat for the other CSV files.
6.  You can now use the Power BI report builder to create charts, graphs, and tables to analyze your habits and productivity.
