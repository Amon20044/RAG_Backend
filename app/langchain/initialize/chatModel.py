import getpass
import os
from dotenv import load_dotenv
load_dotenv()
if not os.getenv("TOGETHER_API_KEY"):
  os.environ["TOGETHER_API_KEY"] = getpass.getpass("Enter API key for Together AI: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", model_provider="together")