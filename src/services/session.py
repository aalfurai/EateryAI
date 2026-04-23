from schemas.user import User
from services.data import DataService


class SessionService:
    """Holds state for a single user session."""

    def __init__(self, data_service: DataService):
        self.data  = data_service
        self._user: User | None = None

    def load_user(self, user_id: str) -> User:
        if self._user is None or self._user.user_id != user_id:
            self._user = self.data.load_user(user_id)
        return self._user

    @property
    def user(self) -> User:
        if self._user is None:
            raise ValueError("No user loaded. Call load_user() first.")
        return self._user

    # NOTE: this is where user preference loops should update
    def update_constraints(self, **kwargs):
        self.user.update_constraints(**kwargs)

    def update_weights(self, **kwargs):
        self.user.update_weights(**kwargs)