#!/usr/bin/env python3
"""
Script to clear all data from the Excellence Tutorial database
while preserving user accounts and admin accounts.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import User, Profile, Fee, Payment, Mark, Notification, Setting, Resource, DropoutRequest, PDF

def clear_all_data():
    # Delete all data from all tables
    for model in [Profile, Fee, Payment, Mark, Notification, Setting, Resource, DropoutRequest, PDF, User]:
        db.session.query(model).delete()
    db.session.commit()
    print("All data cleared from all tables.")

def confirm_clear_data():
    """Ask for confirmation before clearing data"""
    print("⚠️  WARNING: This will permanently delete ALL data!")
    print("   • All tests and marks will be deleted")
    print("   • All fees and payments will be deleted")
    print("   • All notifications will be deleted")
    print("   • All PDFs will be deleted")
    print("   • All resources will be deleted")
    print("   • All settings will be deleted")
    print("   • All profile data will be reset")
    print("\n   ✅ User accounts will be preserved")
    print("   ✅ Admin accounts will be preserved")
    
    response = input("\n🤔 Are you sure you want to continue? (yes/no): ").lower().strip()
    return response in ['yes', 'y']

if __name__ == "__main__":
    print("🧹 Excellence Tutorial - Data Cleanup Script")
    print("=" * 50)
    
    if confirm_clear_data():
        app = create_app()
        with app.app_context():
            clear_all_data()
            print("\n🎯 Data cleanup completed successfully!")
    else:
        print("\n🚫 Data cleanup cancelled.")
        sys.exit(0) 