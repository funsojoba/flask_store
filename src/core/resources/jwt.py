from flask_jwt_extended import create_access_token


class JWTClient:
    def __init__(self, config):
        self.jwt_expiry = config.JWT_ACCESS_TOKEN_EXPIRES

    def create_token(self, user_id):
        identity = {
            "user_id": user_id,
        }
        access_token = create_access_token(identity=identity)

        tokens = {"access_token": access_token}
        return tokens

    def get_user_id(self, jwt_identity):
        return jwt_identity.get("user_id")
