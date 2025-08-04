# utils/chat_utils.py
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

def init_memory() -> ConversationBufferMemory:
    """
    Initialize a conversation memory instance.

    Returns:
        ConversationBufferMemory: A memory object that stores conversation history as messages.
    """
    return ConversationBufferMemory(return_messages=True)


def get_chat_response(prompt: str, memory: ConversationBufferMemory, api_key: str) -> str:
    """
    Generate a response using OpenAI's chat model with conversational memory.

    Args:
        prompt (str): The user's input prompt.
        memory (ConversationBufferMemory): Memory to store and retrieve conversation context.
        api_key (str): OpenAI API key.

    Returns:
        str: The generated response from the model.
    """
    # Initialize the OpenAI chat model
    model = ChatOpenAI(
        model="gpt-4-turbo",
        openai_api_key=api_key
    )
    # Create a conversation chain and invoke the model
    chain = ConversationChain(llm=model, memory=memory)
    result = chain.invoke({"input": prompt})
    return result["response"]
