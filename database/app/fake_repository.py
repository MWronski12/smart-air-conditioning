from typing import Dict, Any, List, Optional
from .database_repository import DatabaseRepository
from .exceptions import *


class FakeRepository(DatabaseRepository):
    def __init__(self):
        self.rooms = {}
        self.devices = {}
        self.users = {}
        self.room_users = {}
        self.room_devices = {}

    def add_room(self, room: Dict[str, Any]) -> Dict[str, Any]:
        if room["id"] in self.rooms:
            raise RoomAlreadyExistsError(f"Room {room['id']} already exists")
        self.rooms[room["id"]] = room

        return room

    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        return self.rooms.get(room_id)

    def get_all_rooms(self) -> List[Dict[str, Any]]:
        return list(self.rooms.values())

    def add_device(self, room_id: str, device: Dict[str, Any]) -> Dict[str, Any]:
        if device["id"] in self.devices:
            raise DeviceAlreadyExistsError(f"Device {device['id']} already exists")
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        self.devices[device["id"]] = device
        if room_id not in self.room_devices:
            self.room_devices[room_id] = {}
        self.room_devices[room_id][device["id"]] = True

        return device

    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")
        if room_id in self.room_devices:
            return [self.devices[dev_id] for dev_id in self.room_devices[room_id]]
        return []

    def add_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        if user["id"] in self.users:
            raise UserAlreadyExistsError(f"User {user['id']} already exists")
        self.users[user["id"]] = user
        return user

    def get_user(self, user_id: str) -> Dict[str, Any]:
        if user_id not in self.users:
            raise UserNotFoundError(f"User {user_id} does not exist")
        return self.users[user_id]

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        if user_id not in self.users:
            raise UserNotFoundError(f"User {user_id} does not exist")
        self.users[user_id]["preferences"] = preferences
        return preferences

    def add_user_to_room(self, user_id: str, room_id: str) -> None:
        if user_id not in self.users:
            raise UserNotFoundError(f"User {user_id} does not exist")
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        if room_id not in self.room_users:
            self.room_users[room_id] = {}
        self.room_users[room_id][user_id] = True

    def remove_user_from_room(self, user_id: str, room_id: str) -> None:
        if user_id not in self.users:
            raise UserNotFoundError(f"User {user_id} does not exist")
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        if room_id in self.room_users and user_id in self.room_users[room_id]:
            del self.room_users[room_id][user_id]

    def get_users_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        if room_id not in self.rooms:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        if room_id in self.room_users:
            return [self.users[user_id] for user_id in self.room_users[room_id]]
        return []
