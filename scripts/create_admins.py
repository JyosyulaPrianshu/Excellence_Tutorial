import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()
from app import create_app
from app.models import create_admin_from_env

app = create_app()
with app.app_context():
    create_admin_from_env() 