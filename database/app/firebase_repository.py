import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, List, Optional, Any

from .database_repository import DatabaseRepository
from .exceptions import *


class FirebaseRepository(DatabaseRepository):
    def __init__(self):
        cred = credentials.Certificate("path/to/serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {"databaseURL": "https://your-project.firebaseio.com"})

    def add_room(self, room: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"rooms/{room['id']}")
        if ref.get() is not None:
            raise RoomAlreadyExistsError(f"Room {room['id']} already exists")

        ref.set({"name": room["name"]})
        return room

    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        ref = db.reference(f"rooms/{room_id}")
        room = ref.get()
        if room is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        return {"id": room_id, "name": room["name"]}

    def get_all_rooms(self) -> List[Dict[str, Any]]:
        ref = db.reference(f"rooms")
        rooms = ref.get()
        return [{"id": room_id, "name": room["name"]} for room_id, room in rooms.items()]

    def add_device(self, room_id: str, device: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"devices/{device['id']}")

        # Check if device already exists
        if ref.get() is not None:
            raise DeviceAlreadyExistsError(f"Device {device['id']} already exists")

        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        ref.set({"name": device["name"]})
        ref = db.reference(f"rooms_devices/{room_id}/{device['id']}")
        ref.set(True)

        return device

    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        ref = db.reference(f"rooms_devices/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        dev_ids = ref.get()
        devices = []
        for dev_id in dev_ids:
            ref = db.reference(f"devices/{dev_id}")
            device = ref.get()
            devices.append(device)

        return devices

    def add_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"users/{user['id']}")
        if ref.get() is not None:
            raise UserAlreadyExistsError(f"User {user['id']} already exists")

        ref.set({"name": user["name"]})
        if "preferences" in user:
            ref = db.reference(f"users/{user['id']}")
            ref.set(user["preferences"])

        return {"id": user["id"], "name": user["name"]}

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        ref = db.reference(f"users/{user_id}")
        user = ref.get()
        if user is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        return {"id": user_id, "name": user["name"]}

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> None:
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        ref.set(preferences)

    def add_user_to_room(self, user_id: str, room_id: str) -> None:
        # Check if user exists
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        ref = db.reference(f"room_users/{room_id}/{user_id}")
        ref.set(True)

    def remove_user_from_room(self, user_id: str, room_id: str) -> None:
        # Check if user exists
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        ref = db.reference(f"room_users/{room_id}/{user_id}")
        ref.delete()

    def get_users_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        ref = db.reference(f"room_users/{room_id}")
        user_ids = ref.get()
        users = []
        for user_id in user_ids:
            ref = db.reference(f"users/{user_id}")
            user = ref.get()
            users.append(user)
        return users
