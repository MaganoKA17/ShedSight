import requests
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, ESKOMPUSH_API_KEY

supabse = create_client(SUPABASE_URL, SUPABASE_KEY)