import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, List, Optional, Any

from .database_repository import DatabaseRepository
from .exceptions import *


class FirebaseRepository(DatabaseRepository):
    def __init__(self):
        cred = credentials.Certificate("pbl5-firebase-admin-key.json")
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": "https://pbl5-5d9d2-default-rtdb.europe-west1.firebasedatabase.app/"},
        )

    def add_room(self, room: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"rooms/{room['id']}")
        if ref.get() is not None:
            raise RoomAlreadyExistsError(f"Room {room['id']} already exists")

        ref.set({"name": room["name"]})
        return room

    def get_room(self, room_id: str) -> Dict[str, Any]:
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
        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        ref = db.reference(f"devices/{device['id']}")

        # Check if device already exists
        if ref.get() is not None:
            raise DeviceAlreadyExistsError(
                f"Device {device['id']} already exists")

        ref.set({"name": device["name"]})
        ref = db.reference(f"rooms_devices/{room_id}/{device['id']}")
        ref.set(True)

        return device

    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        ref = db.reference(f"rooms_devices/{room_id}")
        dev_ids = ref.get()
        if dev_ids is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

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

        ref.set({"email": user["email"]})
        if "preferences" in user:
            ref = db.reference(f"users/{user['id']}")
            ref.set(user["preferences"])

        return {"id": user["id"], "email": user["email"]}

    def get_user(self, user_id: str) -> Dict[str, Any]:
        ref = db.reference(f"users/{user_id}")
        user = ref.get()
        if user is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        return {"id": user_id, "email": user["email"]}

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        ref.update(preferences)
        return preferences

    def add_user_to_room(self, user_id: str, room_id: str) -> None:
        # Check if user exists
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        # Check if room exists
        new_room_ref = db.reference(f"rooms/{room_id}")
        if new_room_ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        rooms_ref = db.reference(f"rooms")
        rooms = rooms_ref.get()
        if rooms:
            for room_key, room_value in rooms.items():
                room_user_ref = db.reference(
                    f"room_users/{room_key}/{user_id}")
                if room_user_ref.get() is not None:
                    room_user_ref.set(False)

        new_ref = db.reference(f"room_users/{room_id}/{user_id}")
        new_ref.set(True)

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

    def get_user_room(self, user_id: str) -> Optional[Dict[str, Any]]:
        room = None
        rooms_users_ref = db.reference("rooms_users")
        rooms_users = rooms_users_ref.get()
        for found_room_id, found_user_id in rooms_users.items():
            if found_user_id == user_id:
                room = db.reference(f"rooms/{found_room_id}").get()

        return room
