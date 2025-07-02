from dotenv import load_dotenv
load_dotenv()
from app import create_app
from app.models import User, db

app = create_app()
with app.app_context():
    admins = User.query.filter_by(is_admin=True).all()
    for admin in admins:
        print(f"Deleting admin: {admin.email}")
        db.session.delete(admin)
    db.session.commit()
    print(f"Deleted {len(admins)} admin(s) from the database.") 