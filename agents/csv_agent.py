# agents/csv_agent.py
from utils.csv_utils import run_csv_agent

class CsvAgent:
    """
    CSV Data Analysis Agent that utilizes the LangChain DataFrame Agent 
    to handle queries and visualization requests.
    """
    def __init__(self, api_key: str, df):
        """
        Initialize the CsvAgent.

        Args:
            api_key (str): OpenAI API key.
            df (pandas.DataFrame): The dataset to be analyzed.
        """
        self.api_key = api_key
        self.df = df

    def run(self, query: str) -> dict:
        """
        Execute the DataFrame Agent to process user queries or visualization requests.

        Args:
            query (str): User's natural language query or visualization requirement.

        Returns:
            dict: JSON response containing 'answer', 'table', 
                  and optionally visualization types like 'bar', 'line', or 'scatter'.
        """
        return run_csv_agent(self.api_key, self.df, query)
