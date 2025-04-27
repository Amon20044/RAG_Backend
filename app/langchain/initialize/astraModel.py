from langchain_astradb import AstraDBVectorStore
import os
from app.langchain.initialize.embedModel import embeddings
from dotenv import load_dotenv
load_dotenv()
# Config
ASTRA_ENDPOINT = os.getenv("ASTRA_ENDPOINT")
ASTRA_TOKEN = os.getenv("ASTRA_TOKEN")
ASTRA_NAMESPACE = os.getenv("ASTRA_NAMESPACE")
COLLECTION_NAME = "lang_1"  # ✅ Fixed collection name

# Safe Initialization
async def get_vector_store_for_chat():
    vector_store = AstraDBVectorStore(
        embedding=embeddings,
        api_endpoint=ASTRA_ENDPOINT,
        token=ASTRA_TOKEN,
        namespace=ASTRA_NAMESPACE,
        collection_name=COLLECTION_NAME
    )
    return vector_store
