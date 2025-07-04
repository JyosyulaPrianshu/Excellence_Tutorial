from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, inspect

load_dotenv()
db_url = os.getenv('SQLALCHEMY_DATABASE_URI')

if not db_url:
    print('No SQLALCHEMY_DATABASE_URI found in environment.')
    exit(1)

engine = create_engine(db_url)
inspector = inspect(engine)

print('Tables and columns in the database:')
for table_name in inspector.get_table_names():
    print(f'\nTable: {table_name}')
    columns = inspector.get_columns(table_name)
    for col in columns:
        print(f"  - {col['name']} ({col['type']})") 