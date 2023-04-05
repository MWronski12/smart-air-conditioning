from firebase_admin import db


class FirebaseRTDB:
    @staticmethod
    def get(path: str):
        return db.reference(path).get()

    @staticmethod
    def add(path: str, data: dict):
        ref = db.reference(path)
        ref.set(data)

    @staticmethod
    def update(path: str, data: dict):
        ref = db.reference(path)
        ref.update(data)
