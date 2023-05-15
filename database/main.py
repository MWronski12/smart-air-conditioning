from app import serve
# from app.fake_repository import FakeRepository
from app.firebase_repository import FirebaseRepository

if __name__ == "__main__":
    repository = FirebaseRepository()
    serve(repository=repository)
