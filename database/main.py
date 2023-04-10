from app import serve
from app.fake_repository import FakeRepository

if __name__ == "__main__":
    repository = FakeRepository()
    serve(repository=repository)
