import core.settings as config
from app.users.models import User
from core.error_handlers import AppError
from core.resources.jwt import JWTClient
from core.utils.utils import BaseService


class SessionTokenService(BaseService):
    model = User
    jwt_client = JWTClient(config)

    def generate_token(self, data):
        email = data.get("email")
        password = data.get("password")

        user = self.model.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            self.logger.error(
                "SessionTokenService.generate_token(): Invalid Credentials for user: %s",
                email,
            )
            raise AppError(401, "Invalid Credentials")

        jwt_token = self.jwt_client.create_token(user.id)

        return jwt_token
