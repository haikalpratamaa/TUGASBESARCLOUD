from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from .models import User

    if not str(user_id).isdigit():
        return None
    return db.session.get(User, int(user_id))
