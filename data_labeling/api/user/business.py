from data_labeling.api.database import db
from data_labeling.api.database.models import User


def create_user(username: str, password: str) -> int:
    new_user = User(password, password)
    found = User.query.filter_by(username=username).first()
    # Todo: handle duplicate username

    db.session.add(new_user)
    db.session.commit()
    return 123