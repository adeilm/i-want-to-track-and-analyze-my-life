# i-want-to-track-and-analyze-my-life

Automate and analyze life tracking by fetching your Habitica data into structured CSV files. Use the output in Power BI, Tableau, or Python notebooks to explore streaks, trends, and completion rates.

## Current Features

- **Automated Data Fetching:** Pulls your latest data directly from the Habitica API.
- **Structured Storage:** Organizes your data into clear, easy-to-use CSV files under `DataBase/` (`habits.csv`, `dailies.csv`, `todos.csv`, `rewards.csv`).
- **Ready for Visualization:** The CSV output is designed to be easily imported into tools like Power BI, Tableau, or Google Sheets for analysis.
- **Portable Paths:** No hard-coded absolute paths; uses `os.path.join`.
- **Basic Error Handling:** Clear messages when credentials are missing or API calls fail.

## Getting Started

Follow these instructions to get your own copy of the project up and running.

### Prerequisites

- Python 3.6+
- A Habitica account

### Installation

1.  Clone the repository:
    ```sh
    git clone https://github.com/adeilm/i-want-to-track-and-analyze-my-life.git
    cd i-want-to-track-and-analyze-my-life
    ```

2.  Create and activate a virtual environment (recommended):
    ```sh
    python -m venv venv
    venv\Scripts\activate
    
    ```

3.  Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

### Configuration

1.  Create a `.env` file in the repository root with:
    ```dotenv
    HABITICA_USER_ID=your_user_id_here
    HABITICA_API_TOKEN=your_api_token_here
    ```

   How to find these values:
   - Log in to your [Habitica](https://habitica.com) account
   - Go to Settings → API
   - Copy your User ID and API Token

### Usage

Run the main script to fetch your data and generate the CSV files:

```sh
python src/process_data.py
```

Output files will be saved to the `DataBase/` directory:
- `DataBase/habits.csv`
- `DataBase/dailies.csv`
- `DataBase/todos.csv`
- `DataBase/rewards.csv`

## Visualization

You can now use the generated CSV files to create dashboards and visualizations.

### Example with Power BI

1.  Open Power BI Desktop.
2.  Click **Get Data** and select **Text/CSV**.
3.  Navigate to the `DataBase/` directory and select one of the CSV files (e.g., `dailies.csv`).
4.  Power BI will automatically detect the headers and data types. Click **Load**.
5.  Repeat for the other CSV files.
6.  You can now use the Power BI report builder to create charts, graphs, and tables to analyze your habits and productivity.

## Roadmap (Planned / In Progress)

- Debug and fix errors in Python scripts as they arise
- Track additional Habitica data: rewards, user stats, achievements
- Improve processing with robust error handling, logging, and data validation
- Optimize performance for large datasets (batching, incremental runs)
- Extend Habitica API integration (user profile, party data, challenges)
- Integrate other life-tracking APIs (fitness trackers, calendar, time tracking)
- Webhook integration for near real-time updates
- Data pipeline automation with proper error recovery and retries
- Better documentation and examples

## Code Documentation

- Public functions and classes include docstrings in source files under `src/`
- Future plan: generate HTML docs with `pdoc` or `Sphinx`

## Error Handling and Logging

- Uses Python `logging` with timestamps and levels
- Improved messages for missing credentials and failed API calls
- Planned: structured logging and schema validation

## Performance Considerations

- Suitable for typical Habitica data sizes
- Planned optimizations:
  - Batch writes / streaming CSV for large exports
  - Incremental updates to avoid reprocessing unchanged items

## Contributing

- Use Python 3.10+
- Keep functions documented with docstrings
- Prefer small, focused pull requests
- Add or update tests for processing logic
- Run linters/formatters if configured
