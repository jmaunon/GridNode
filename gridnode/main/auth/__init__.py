import json
import functools
from flask_login import LoginManager, current_user, UserMixin
from .. import local_worker

from .user_session import UserSession
from .session_repository import SessionsRepository

SESSION_TYPES = [UserSession]
session_repository = None
login_manager = LoginManager()


def set_auth_configs(app):
    """ Set configs to use flask session manager

        Args:
            app: Flask application
        Returns:
            app: Flask application
    """
    global session_repository
    login_manager.init_app(app)
    session_repository = SessionsRepository()
    return app


def get_session():
    """ Returns the global instance of session repository. """
    global session_repository
    return session_repository


# callback to reload the user object
@login_manager.user_loader
def load_user(userid: str) -> UserMixin:
    """ Retrieve user session object from session repository.

        Args:
            userid (str) : User id.
        Returns:
            user : User Session.
    """
    return session_repository.get_session_by_id(userid)


def authenticated_only(f):
    """ Custom Wrapper to check and route authenticated user sessions.

        Args:
            f (function) : Function to be used by authenticated users.
        Returns:
            response : Function result.
    """

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            current_user.worker = local_worker
            return f(*args, **kwargs)
        else:
            return f(*args, **kwargs)

    return wrapped
