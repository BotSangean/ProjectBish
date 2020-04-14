from userbot.modules.sql_helper import SESSION, BASE
from sqlalchemy import Column, LargeBinary, Integer
import threading


class GoogleDriveCreds(BASE):
    __tablename__ = 'creds'
    user = Column(Integer, primary_key=True)
    credentials = Column(LargeBinary)

    def __init__(self, user):
        self.user = user


GoogleDriveCreds.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def save_credentials(user, credentials):
    with INSERTION_LOCK:
        saved_credentials = get_credentials(user)
        if not saved_credentials:
            saved_credentials = GoogleDriveCreds(user)

            SESSION.add(saved_credentials)
            SESSION.commit()
            return True


def get_credentials(user):
    with INSERTION_LOCK:
        try:
            saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
            creds = None

            if saved_credentials is not None:
                creds = saved_credentials.credentials
            return creds
        finally:
            SESSION.close()


def clear_credentials(user):
    with INSERTION_LOCK:
        saved_credentials = SESSION.query(GoogleDriveCreds).get(user)
        if saved_credentials:
            SESSION.delete(saved_credentials)
            SESSION.commit()
            return True
