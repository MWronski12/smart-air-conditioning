import firebase_admin
from firebase_admin import credentials, db
from typing import List, Dict, Any

from .database_repository import DatabaseRepository


class FirebaseSmartAcRepository(DatabaseRepository):
    def __init__(self):
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://your-project.firebaseio.com"})

    def add_room(self, room: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"project/rooms/{room_id}")
        ref.set({"name": name})

    def get_room(self, room_id: str) -> Dict[str, Any]:
        ref = db.reference(f"project/rooms/{room_id}")
        return ref.get()

    def create_user(self, user_id: str, name: str, email: str):
        ref = db.reference(f"project/users/{user_id}")
        ref.set(
            {
                "name": name,
                "email": email,
                "preferences": {
                    "temperature": None,
                    "fan_speed": None,
                },
            }
        )

    def get_user(self, user_id: str) -> Dict[str, Any]:
        ref = db.reference(f"project/users/{user_id}")
        return ref.get()

    def create_device(self, device_id: str, name: str, type_: str, user_id: str, room_id: str, status: str):
        ref = db.reference(f"project/rooms/{room_id}/devices/{device_id}")
        ref.set(
            {
                "name": name,
                "type": type_,
                "user_id": user_id,
                "status": status,
            }
        )

    def get_device(self, device_id: str) -> Dict[str, Any]:
        ref = db.reference(f"project/rooms")
        rooms = ref.get()
        for room_id in rooms:
            devices = rooms[room_id]["devices"]
            if device_id in devices:
                return devices[device_id]

    def get_users_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        ref = db.reference(f"project/room_users/{room_id}")
        users = ref.get()
        return [{"id": user_id, **user} for user_id, user in users.items()]

    def add_user_to_room(self, user_id: str, room_id: str):
        ref = db.reference(f"project/room_users/{room_id}/{user_id}")
        ref.set(True)

    def get_all_rooms(self) -> List[Dict[str, Any]]:
        ref = db.reference(f"project/rooms")
        rooms = ref.get()
        return [{"id": room_id, **room} for room_id, room in rooms.items()]

    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        ref = db.reference(f"project/rooms/{room_id}/devices")
        devices = ref.get()
        return [{"id": device_id, **device} for device_id, device in devices.items()]
