from flask import Flask, jsonify
from flask_cors import CORS
from groq import Groq
from supabase import create_client
import sys
sys.path.append("../pipeline")
from config import SUPABASE_URL, SUPABASE_KEY, GROQ_API_KEY

app = Flask(__name__)
CORS(app)

supabase =create_client(SUPABASE_URL, SUPABASE_KEY)
client = Groq(api_key=GROQ_API_KEY)

