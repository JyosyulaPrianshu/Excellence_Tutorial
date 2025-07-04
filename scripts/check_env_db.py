from dotenv import load_dotenv
import os

load_dotenv()

print('SQLALCHEMY_DATABASE_URI:', os.getenv('SQLALCHEMY_DATABASE_URI')) 