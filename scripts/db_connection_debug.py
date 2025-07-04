#!/usr/bin/env python3
"""
Comprehensive Database Connection Debugging Script
Tests various connection methods and provides detailed diagnostics
"""

import os
import sys
import socket
import ssl
import time
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_section(title):
    print(f"\n📋 {title}")
    print("-" * 40)

def test_environment_variables():
    """Test environment variable loading"""
    print_section("Environment Variables")
    
    db_url = os.getenv('SQLALCHEMY_DATABASE_URI')
    if not db_url:
        print("❌ SQLALCHEMY_DATABASE_URI not found in environment")
        return None
    
    print(f"✅ SQLALCHEMY_DATABASE_URI found")
    print(f"   Type: {'PostgreSQL' if 'postgresql' in db_url else 'SQLite' if 'sqlite' in db_url else 'Unknown'}")
    
    # Parse the URL
    try:
        parsed = urlparse(db_url)
        print(f"   Host: {parsed.hostname}")
        print(f"   Port: {parsed.port}")
        print(f"   Database: {parsed.path[1:] if parsed.path else 'None'}")
        print(f"   Username: {parsed.username}")
        print(f"   SSL: {'Yes' if parsed.scheme == 'postgresql' else 'No'}")
    except Exception as e:
        print(f"   ❌ Error parsing URL: {e}")
        return None
    
    return db_url

def test_network_connectivity(hostname, port):
    """Test basic network connectivity"""
    print_section("Network Connectivity")
    
    try:
        # Test DNS resolution
        print(f"🔍 Resolving hostname: {hostname}")
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS Resolution: {hostname} → {ip_address}")
        
        # Test TCP connection
        print(f"🔍 Testing TCP connection to {hostname}:{port}")
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((hostname, port))
        end_time = time.time()
        
        if result == 0:
            print(f"✅ TCP Connection: SUCCESS ({end_time - start_time:.2f}s)")
            sock.close()
            return True
        else:
            print(f"❌ TCP Connection: FAILED (Error code: {result})")
            sock.close()
            return False
            
    except socket.gaierror as e:
        print(f"❌ DNS Resolution failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Network test failed: {e}")
        return False

def test_ssl_connection(hostname, port):
    """Test SSL connection"""
    print_section("SSL Connection Test")
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        print(f"🔍 Testing SSL connection to {hostname}:{port}")
        start_time = time.time()
        
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                end_time = time.time()
                print(f"✅ SSL Connection: SUCCESS ({end_time - start_time:.2f}s)")
                print(f"   SSL Version: {ssock.version()}")
                print(f"   Cipher: {ssock.cipher()[0]}")
                return True
                
    except Exception as e:
        print(f"❌ SSL Connection failed: {e}")
        return False

def test_postgresql_connection(db_url):
    """Test PostgreSQL connection with different methods"""
    print_section("PostgreSQL Connection Tests")
    
    # Test 1: Basic psycopg2 connection
    try:
        import psycopg2
        print("🔍 Testing with psycopg2...")
        
        parsed = urlparse(db_url)
        conn_params = {
            'host': parsed.hostname,
            'port': parsed.port,
            'database': parsed.path[1:],
            'user': parsed.username,
            'password': parsed.password,
            'sslmode': 'require',
            'connect_timeout': 10
        }
        
        start_time = time.time()
        conn = psycopg2.connect(**conn_params)
        end_time = time.time()
        
        print(f"✅ psycopg2 Connection: SUCCESS ({end_time - start_time:.2f}s)")
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"   PostgreSQL Version: {version.split(',')[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("⚠️  psycopg2 not installed")
    except Exception as e:
        print(f"❌ psycopg2 Connection failed: {e}")
    
    # Test 2: SQLAlchemy connection
    try:
        from sqlalchemy import create_engine
        print("🔍 Testing with SQLAlchemy...")
        
        engine = create_engine(db_url, 
                             connect_args={'sslmode': 'require'},
                             pool_pre_ping=True,
                             pool_recycle=300)
        
        start_time = time.time()
        with engine.connect() as conn:
            end_time = time.time()
            print(f"✅ SQLAlchemy Connection: SUCCESS ({end_time - start_time:.2f}s)")
            
            # Test query
            result = conn.execute("SELECT version();")
            version = result.fetchone()[0]
            print(f"   PostgreSQL Version: {version.split(',')[0]}")
            
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy Connection failed: {e}")
    
    return False

def test_flask_app_connection():
    """Test Flask app database connection"""
    print_section("Flask App Database Connection")
    
    try:
        from app import create_app, db
        
        print("🔍 Creating Flask app...")
        app = create_app()
        
        print("🔍 Testing database connection within Flask context...")
        with app.app_context():
            start_time = time.time()
            db.engine.execute("SELECT 1")
            end_time = time.time()
            print(f"✅ Flask Database Connection: SUCCESS ({end_time - start_time:.2f}s)")
            return True
            
    except Exception as e:
        print(f"❌ Flask Database Connection failed: {e}")
        return False

def check_firewall_and_proxy():
    """Check for common firewall and proxy issues"""
    print_section("Firewall & Proxy Analysis")
    
    # Check if we're behind a proxy
    http_proxy = os.getenv('HTTP_PROXY') or os.getenv('http_proxy')
    https_proxy = os.getenv('HTTPS_PROXY') or os.getenv('https_proxy')
    
    if http_proxy or https_proxy:
        print(f"⚠️  Proxy detected:")
        if http_proxy:
            print(f"   HTTP_PROXY: {http_proxy}")
        if https_proxy:
            print(f"   HTTPS_PROXY: {https_proxy}")
        print("   This might interfere with direct database connections")
    else:
        print("✅ No proxy detected")
    
    # Check Windows Firewall (if on Windows)
    if os.name == 'nt':
        print("🔍 Windows Firewall check:")
        try:
            import subprocess
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("✅ Windows Firewall status retrieved")
                if "ON" in result.stdout:
                    print("   ⚠️  Windows Firewall is ON - may block connections")
            else:
                print("   ⚠️  Could not check Windows Firewall status")
        except Exception as e:
            print(f"   ⚠️  Windows Firewall check failed: {e}")

def suggest_solutions():
    """Provide solution suggestions based on findings"""
    print_section("Recommended Solutions")
    
    print("🔧 Based on the diagnostics, try these solutions:")
    print("\n1. **Network Issues:**")
    print("   - Try connecting from a different network (mobile hotspot)")
    print("   - Check if your ISP blocks port 5432")
    print("   - Try using a different VPN server")
    
    print("\n2. **Firewall Issues:**")
    print("   - Temporarily disable Windows Firewall")
    print("   - Check router settings for port blocking")
    print("   - Add exception for PostgreSQL connections")
    
    print("\n3. **Database Configuration:**")
    print("   - Verify the External Database URL from Render")
    print("   - Check if database access control allows your IP")
    print("   - Ensure SSL is properly configured")
    
    print("\n4. **Alternative Solutions:**")
    print("   - Use a different database provider (Supabase, Railway)")
    print("   - Set up a local PostgreSQL for development")
    print("   - Use database tunneling (ngrok, localtunnel)")

def main():
    print_header("Database Connection Diagnostics")
    
    # Test environment variables
    db_url = test_environment_variables()
    if not db_url:
        print("\n❌ Cannot proceed without database URL")
        return
    
    # Parse URL for network tests
    parsed = urlparse(db_url)
    hostname = parsed.hostname
    port = parsed.port or 5432
    
    # Test network connectivity
    network_ok = test_network_connectivity(hostname, port)
    
    # Test SSL if network is ok
    if network_ok:
        ssl_ok = test_ssl_connection(hostname, port)
    else:
        ssl_ok = False
    
    # Test PostgreSQL connections
    if network_ok:
        pg_ok = test_postgresql_connection(db_url)
    else:
        pg_ok = False
    
    # Test Flask app connection
    flask_ok = test_flask_app_connection()
    
    # Check firewall and proxy
    check_firewall_and_proxy()
    
    # Summary
    print_header("Diagnostic Summary")
    print(f"Network Connectivity: {'✅ PASS' if network_ok else '❌ FAIL'}")
    print(f"SSL Connection: {'✅ PASS' if ssl_ok else '❌ FAIL'}")
    print(f"PostgreSQL Connection: {'✅ PASS' if pg_ok else '❌ FAIL'}")
    print(f"Flask App Connection: {'✅ PASS' if flask_ok else '❌ FAIL'}")
    
    if not network_ok:
        print("\n🚨 PRIMARY ISSUE: Network connectivity failed")
        print("   This suggests a firewall, ISP, or network configuration issue")
    elif not ssl_ok:
        print("\n🚨 PRIMARY ISSUE: SSL connection failed")
        print("   This suggests SSL configuration or certificate issues")
    elif not pg_ok:
        print("\n🚨 PRIMARY ISSUE: PostgreSQL authentication failed")
        print("   This suggests database credentials or access control issues")
    elif not flask_ok:
        print("\n🚨 PRIMARY ISSUE: Flask app configuration issue")
        print("   This suggests application-level configuration problems")
    else:
        print("\n✅ All tests passed! Database connection should work.")
    
    # Provide solutions
    suggest_solutions()

if __name__ == "__main__":
    main() 