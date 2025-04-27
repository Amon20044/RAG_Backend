import os
from supabase import create_client, Client
from dotenv import load_dotenv
load_dotenv()
# Ensure your environment variables are set correctly
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

# Create the sync client
supabase: Client = create_client(url, key)

# Example of querying data
response = supabase.table("users").select("*").execute()
print(response)
