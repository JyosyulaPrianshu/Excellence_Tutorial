from app import create_app
from app.models import User

def count_users():
    admin_count = User.query.filter_by(is_admin=True).count()
    student_count = User.query.filter_by(is_admin=False).count()
    total = User.query.count()
    print(f"Total users: {total}")
    print(f"Admins: {admin_count}")
    print(f"Students: {student_count}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        count_users() 