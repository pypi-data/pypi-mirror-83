from datetime import datetime, timedelta
from uuid import uuid4

from app import db
from auth_users.authentication.exceptions import AuthRefreshTokenExpired, AuthRefreshTokenInvalid

# Token valid for an hour
TOKEN_PERIOD = 1
# Refresh Token valid for 24 hour
REFRESH_TOKEN_PERIOD = 24


def create_auth_tokens(user_id: int, auth_model) -> dict:
    # When creating new tokens, delete other tokens for that user
    auth_token = db.session.query(auth_model).filter_by(user_id=user_id).first()

    expiry_date = datetime.now() + timedelta(hours=TOKEN_PERIOD)
    refresh_expiry_time = datetime.now() + timedelta(hours=REFRESH_TOKEN_PERIOD)

    if not auth_token:
        b = dict(
            expiry_date=expiry_date,
            refresh_expiry_time=refresh_expiry_time,
            user_id=user_id,
        )
        auth_token = auth_model(**b)
        auth_token.save_instance()

    else:
        auth_token.expiry_date = expiry_date
        auth_token.refresh_expiry_time = refresh_expiry_time
        auth_token.refresh_token = uuid4()
        auth_token.token = uuid4()
        auth_token.save_instance()

    return dict(
        refresh_token=auth_token.refresh_token,
        token=auth_token.token,
    )


def verify_token(token: str, auth_model):
    auth_token = db.session.query(auth_model).filter_by(token=token).first()

    if not auth_token:
        raise AuthRefreshTokenInvalid()

    # Check if refresh_token as expired.
    if datetime.now() > auth_token.expiry_date:
        raise AuthRefreshTokenExpired()


def refresh_token(token: str, auth_model):
    auth_token = db.session.query(auth_model).filter_by(refresh_token=token).first()

    if not auth_token:
        raise AuthRefreshTokenInvalid()

    # Check if refresh_token as expired.
    if (
        datetime.now() >
        datetime.strptime(
            auth_token.refresh_expiry_time, "%Y-%m-%d %H:%M:%S"
        )
    ):
        raise AuthRefreshTokenExpired()

    return create_auth_tokens(auth_token.user_id, auth_model)
