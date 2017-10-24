from flask_user import UserManager

# from data_labeling.api.app import User
from data_labeling.api.database import db

user_manager = UserManager()

def create_user(username: str, password: str) -> int:
    password_hash = user_manager.hash_password(password)
    # all = User.query.all()
    print(all)
    return 1
    # new_user = User(username, password_hash)
    # found = User.query.filter_by(username=username).first()
    print(found)
    # Todo: handle duplicate username

    db.session.add(new_user)
    db.session.commit()
    return 123