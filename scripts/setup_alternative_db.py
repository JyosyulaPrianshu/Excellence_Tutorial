#!/usr/bin/env python3
"""
Setup script for alternative database providers
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_supabase_connection():
    """Test Supabase connection"""
    print("🔍 Testing Supabase connection...")
    
    # You would need to get these from Supabase dashboard
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Supabase credentials not found in .env")
        print("   Add SUPABASE_URL and SUPABASE_ANON_KEY to your .env file")
        return False
    
    try:
        headers = {
            'apikey': supabase_key,
            'Authorization': f'Bearer {supabase_key}'
        }
        
        response = requests.get(f"{supabase_url}/rest/v1/", headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Supabase connection successful")
            return True
        else:
            print(f"❌ Supabase connection failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase connection error: {e}")
        return False

def test_railway_connection():
    """Test Railway connection"""
    print("🔍 Testing Railway connection...")
    
    railway_url = os.getenv('RAILWAY_DATABASE_URL')
    if not railway_url:
        print("❌ Railway database URL not found in .env")
        print("   Add RAILWAY_DATABASE_URL to your .env file")
        return False
    
    try:
        import psycopg2
        from urllib.parse import urlparse
        
        parsed = urlparse(railway_url)
        conn_params = {
            'host': parsed.hostname,
            'port': parsed.port or 5432,
            'database': parsed.path[1:],
            'user': parsed.username,
            'password': parsed.password,
            'sslmode': 'require',
            'connect_timeout': 10
        }
        
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"✅ Railway connection successful: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Railway connection error: {e}")
        return False

def setup_local_postgresql():
    """Setup instructions for local PostgreSQL"""
    print("🔧 Local PostgreSQL Setup Instructions")
    print("=" * 50)
    
    print("\n1. **Install PostgreSQL:**")
    print("   Windows: Download from https://www.postgresql.org/download/windows/")
    print("   Or use Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres")
    
    print("\n2. **Create Database:**")
    print("   - Open pgAdmin or psql")
    print("   - Create database: excellence_tutorial")
    print("   - Create user: excellence_user")
    
    print("\n3. **Update .env file:**")
    print("   SQLALCHEMY_DATABASE_URI=postgresql://excellence_user:password@localhost:5432/excellence_tutorial")
    
    print("\n4. **Run migrations:**")
    print("   flask db upgrade")
    
    print("\n5. **Test connection:**")
    print("   python scripts/test_local_db.py")

def main():
    print("🔧 Alternative Database Setup")
    print("=" * 50)
    
    print("\nSince your network blocks external PostgreSQL connections,")
    print("here are alternative solutions:")
    
    print("\n1. **Local PostgreSQL (Recommended for development)**")
    print("   - Works offline")
    print("   - No network restrictions")
    print("   - Full control")
    
    print("\n2. **Supabase (Cloud alternative)**")
    print("   - Free tier available")
    print("   - Different connection method")
    print("   - May bypass network restrictions")
    
    print("\n3. **Railway (Another cloud option)**")
    print("   - Free tier available")
    print("   - Different infrastructure")
    print("   - May work with your network")
    
    print("\n4. **Mobile Hotspot Test**")
    print("   - Try connecting via phone hotspot")
    print("   - Bypass current network restrictions")
    
    choice = input("\nWhich option would you like to try? (1-4): ").strip()
    
    if choice == "1":
        setup_local_postgresql()
    elif choice == "2":
        test_supabase_connection()
    elif choice == "3":
        test_railway_connection()
    elif choice == "4":
        print("\n📱 Mobile Hotspot Instructions:")
        print("1. Enable mobile hotspot on your phone")
        print("2. Connect your computer to the hotspot")
        print("3. Run: python scripts/db_connection_debug.py")
        print("4. If it works, your current network is blocking PostgreSQL")
    else:
        print("Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main() 