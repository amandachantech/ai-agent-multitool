# agents/chat_agent.py
from utils.chat_utils import init_memory, get_chat_response
from langchain.memory import ConversationBufferMemory

class ChatAgent:
    """
    Chat Agent responsible for handling general conversation functionality.
    """
    def __init__(self, api_key: str, memory: ConversationBufferMemory = None):
        """
        Initialize the ChatAgent.

        Args:
            api_key (str): OpenAI API key.
            memory (ConversationBufferMemory, optional): Existing conversation memory.
                If not provided, a new memory instance will be created.
        """
        self.api_key = api_key
        # Use the provided memory if available; otherwise, initialize a new memory instance.
        self.memory = memory if memory is not None else init_memory()

    def run(self, prompt: str) -> str:
        """
        Generate a response using memory and the model.

        Args:
            prompt (str): The user's input message.

        Returns:
            str: The generated response from the model.
        """
        return get_chat_response(prompt, self.memory, self.api_key)