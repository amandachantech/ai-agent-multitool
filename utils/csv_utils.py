# utils/csv_utils.py
import json
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent

PROMPT_TEMPLATE = """
You are a data analysis assistant. Your response format depends on the type of user request:

1. For text-based answers, respond in the following JSON format:
   {"answer": "<your answer here>"}

2. If the user requests a table, respond in the following format:
   {"table": {"columns": ["column1", "column2", ...], "data": [[value1, value2, ...], [...] ]}}

3. If the user’s request is best represented as a bar chart:
   {"bar": {"columns": ["A", "B", ...], "data": [v1, v2, ...]}}

4. If the request is suitable for a line chart:
   {"line": {"columns": ["A", "B", ...], "data": [v1, v2, ...]}}

5. If the request is suitable for a scatter plot:
   {"scatter": {"columns": ["A", "B", ...], "data": [[x1, y1], [x2, y2], ...]}}

Return **all outputs** strictly as a JSON string with double quotes.

User request:
"""

def run_csv_agent(api_key: str, df, query: str) -> dict:
    """
    Execute a user query on a CSV dataset using LangChain's DataFrame Agent 
    and return the result in JSON format.

    Args:
        api_key (str): OpenAI API key.
        df (pandas.DataFrame): The DataFrame to analyze.
        query (str): User's natural language query or visualization request.

    Returns:
        dict: Parsed JSON result that may include one of the keys: 
              `answer`, `table`, `bar`, `line`, or `scatter`.
    """
    # Initialize the OpenAI chat model
    model = ChatOpenAI(
        model="gpt-4-turbo",
        openai_api_key=api_key,
        temperature=0
    )
    # Create the DataFrame Agent
    agent = create_pandas_dataframe_agent(
        llm=model,
        df=df,
        agent_executor_kwargs={"handle_parsing_errors": True},
        verbose=True
    )
    # Build the prompt and invoke the agent
    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input": prompt})
    # Parse and return JSON output
    return json.loads(response["output"])
