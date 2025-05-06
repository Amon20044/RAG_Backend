import getpass
import os
from dotenv import load_dotenv
load_dotenv()
if not os.getenv("TOGETHER_API_KEY"):
  os.environ["TOGETHER_API_KEY"] = getpass.getpass("Enter API key for Together AI: ")

from langchain.chat_models import init_chat_model

llm = init_chat_model("Qwen/Qwen3-235B-A22B-fp8-tput", model_provider="together")