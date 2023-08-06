from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql.functions import func


class AuthenticateModel:
    """Represents the authtokens table."""

    __tablename__ = 'authtokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False, default=uuid4)
    refresh_token = Column(String, nullable=False, default=uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    expiry_date = Column(DateTime, nullable=True, default=func.now())
    refresh_expiry_time = Column(DateTime, nullable=True, default=func.now())

    def __repr__(self):
        return f'<AuthToken: {self.user_id}'

    def to_dict(self):
        data = self.__dict__
        if data.get('expiry_date'):
            data['expiry_date'] = data.get('expiry_date').strftime('%d/%m/%Y, %H:%M:%S')
        if data.get('refresh_expiry_time'):
            data['refresh_expiry_time'] = (
                data.get('refresh_expiry_time').strftime('%d/%m/%Y, %H:%M:%S')
            )
        if '_sa_instance_state' in data:
            del data['_sa_instance_state']
        return data
