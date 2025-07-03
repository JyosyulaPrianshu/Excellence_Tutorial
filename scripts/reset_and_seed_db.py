from app import create_app, db
from app.models import User, Profile
from werkzeug.security import generate_password_hash

classes = [
    ('6', 'Class 6', '6'),
    ('7', 'Class 7', '7'),
    ('8', 'Class 8', '8'),
    ('9', 'Class 9', '9'),
    ('10', 'Class 10', '10'),
    ('11_arts', 'Class 11 Arts', '11A'),
    ('11_science', 'Class 11 Science', '11S'),
    ('12_arts', 'Class 12 Arts', '12A'),
    ('12_science', 'Class 12 Science', '12S'),
]

STUDENT_PASSWORD = 'student123'
ADMIN_EMAIL = 'admin@eg.com'
ADMIN_PASSWORD = 'admin123'

def reset_and_seed():
    # Delete all data
    db.reflect()
    db.drop_all()
    db.create_all()
    print('All tables dropped and recreated.')

    # Add students
    global_counter = 1
    for class_key, class_label, class_code in classes:
        for i in range(2):
            email = f"student{i+1}_{class_key}@example.com"
            user = User(email=email, password=generate_password_hash(STUDENT_PASSWORD), is_admin=False)
            db.session.add(user)
            db.session.commit()
            reg_no = f"E.T.{class_code}({global_counter:03d})"
            profile = Profile(
                user_id=user.id,
                full_name=f"Student {i+1} {class_label}",
                parent_name=f"Parent {i+1} {class_label}",
                parent_phone=f"90000000{global_counter:02d}",
                student_phone=f"80000000{global_counter:02d}",
                student_class=class_key,
                school_name="Seeded School",
                roll_number=i+1,
                reg_no=reg_no
            )
            db.session.add(profile)
            db.session.commit()
            print(f"Created student: {email} | reg_no: {reg_no}")
            global_counter += 1

    # Add admin
    admin = User(email=ADMIN_EMAIL, password=generate_password_hash(ADMIN_PASSWORD), is_admin=True)
    db.session.add(admin)
    db.session.commit()
    print(f"Created admin: {ADMIN_EMAIL} | password: {ADMIN_PASSWORD}")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        reset_and_seed() 