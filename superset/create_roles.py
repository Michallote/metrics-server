from flask_appbuilder.security.sqla.models import Role, User

from superset import security_manager
from superset.extensions import db


def create_roles_and_users():
    print("🔵 Creating custom roles and users...")

    # Create a new custom role if it doesn't exist
    role_name = "Data Analyst"
    role = security_manager.find_role(role_name)
    if not role:
        role = security_manager.add_role(role_name)

    # You could also assign permissions to the role here if you want

    # Create a user for this role
    username = "analyst"
    email = "analyst@example.com"
    password = "analystpass"  # Ideally inject this via ENV later

    user = security_manager.find_user(username=username)
    if not user:
        user = security_manager.add_user(
            username=username,
            first_name="Data",
            last_name="Analyst",
            email=email,
            role=role,
            password=password,
        )
        print(f"✅ Created user {username} with role {role_name}")

    db.session.commit()

    print("✅ Done creating roles and users.")
