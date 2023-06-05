import os
import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, List, Optional, Any

from .database_repository import DatabaseRepository
from .exceptions import *
import logging

databaseURL = "https://pbl5-5d9d2-default-rtdb.europe-west1.firebasedatabase.app/"


class FirebaseRepository(DatabaseRepository):
    def __init__(self):
        cred = credentials.Certificate("pbl5-firebase-admin-key.json")
        firebase_admin.initialize_app(
            cred,
            {"databaseURL": databaseURL},
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
        if rooms is None:
            return []
        else:
            return [{"id": room_id, "name": room["name"]} for room_id, room in rooms.items()]

    def add_device(self, room_id: str, device: Dict[str, Any]) -> Dict[str, Any]:
        # Check if room exists
        ref = db.reference(f"rooms/{room_id}")
        if ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        # Check if device already exists
        ref = db.reference(f"devices/{device['id']}")
        if ref.get() is not None:
            raise DeviceAlreadyExistsError(f"Device {device['id']} already exists")

        # Set device
        ref = db.reference(f"devices/{device['id']}")
        ref.set({"name": device["name"]})

        # Set device in room
        ref = db.reference(f"rooms_devices/{room_id}")
        ref.update({device["id"]: True})

        return device

    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        # Check if room exists
        room_ref = db.reference(f"rooms/{room_id}")
        if room_ref.get() is None:
            raise RoomNotFoundError(f"Room {room_id} does not exist")

        room_devices_ref = db.reference(f"rooms_devices/{room_id}")
        room_devices = room_devices_ref.get()
        if room_devices is None:
            return []

        devices = []
        for dev_id in room_devices.keys():
            ref = db.reference(f"devices/{dev_id}")
            device = ref.get()
            if device is None:
                raise DeviceNotFoundError(
                    f"Logic error - device is registered in a room, but device details are missing!"
                )
            devices.append({"id": dev_id, "name": device["name"]})

        return devices

    def add_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        # Check if user already exists
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

        room_users_ref = db.reference(f"room_users/{room_id}")
        room_users_ref.update({user_id: True})

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
        room_users = ref.get()
        if room_users is None:
            return []

        users = []
        for user_id in room_users.keys():
            ref = db.reference(f"users/{user_id}")
            user = ref.get()
            if user is None:
                raise UserNotFoundError(
                    f"Logic error - useris registered in a room, but user details are missing!"
                )
            fan_speed = user["fan_speed"] if "fan_speed" in user.keys() else None
            temperature = user["temperature"] if "temperature" in user.keys() else None
            users.append(
                {
                    "id": user_id,
                    "email": user["email"],
                    "fan_speed": fan_speed,
                    "temperature": temperature,
                }
            )

        return users

    def get_user_room(self, user_id: str) -> Optional[Dict[str, Any]]:
        # Check if user exists
        ref = db.reference(f"users/{user_id}")
        if ref.get() is None:
            raise UserNotFoundError(f"User {user_id} does not exist")

        room_users_ref = db.reference("room_users")
        room_users = room_users_ref.get()
        if room_users is None:
            return None

        for room_id in room_users.keys():
            for uid in room_users[room_id].keys():
                if uid == user_id:
                    room = db.reference(f"rooms/{room_id}").get()
                    return {"id": room_id, "name": room["name"]}

        return None
