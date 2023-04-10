import unittest
from os import getenv
from typing import Dict, Any, List, Optional
from app.exceptions import *
from app.fake_repository import FakeRepository


class TestDatabaseRepository(unittest.TestCase):
    def setUp(self):
        self.repo = FakeRepository()

    def test_add_room(self):
        room = {"id": "1", "name": "Bedroom"}
        self.assertEqual(self.repo.add_room(room), room)
        with self.assertRaises(RoomAlreadyExistsError):
            self.repo.add_room(room)

    def test_get_room(self):
        with self.assertRaises(RoomNotFoundError):
            self.repo.get_room("1")
        room = {"id": "1", "name": "Bedroom"}
        self.assertEqual(self.repo.add_room(room), room)
        self.assertEqual(self.repo.get_room("1"), room)

    def test_get_all_rooms(self):
        rooms = [{"id": "1", "name": "Bedroom"}, {"id": "2", "name": "Living Room"}]
        for room in rooms:
            self.assertEqual(self.repo.add_room(room), room)
        self.assertCountEqual(self.repo.get_all_rooms(), rooms)
        self.assertListEqual(rooms, self.repo.get_all_rooms())

    def test_add_device(self):
        room = {"id": "1", "name": "Bedroom"}
        self.assertEqual(self.repo.add_room(room), room)
        device = {"id": "1", "name": "A/C bedroom"}
        self.assertEqual(self.repo.add_device(room["id"], device), device)
        with self.assertRaises(DeviceAlreadyExistsError):
            self.repo.add_device(room["id"], device)
        with self.assertRaises(RoomNotFoundError):
            device = {"id": "2", "name": "A/C living room"}
            self.repo.add_device("non-existent-room", device)

    def test_get_devices_in_room(self):
        room = {"id": "1", "name": "Bedroom"}
        self.repo.add_room(room)
        devices = [
            {"id": "1", "name": "A/C ceiling"},
            {"id": "2", "name": "A/C wall"},
        ]
        for device in devices:
            self.repo.add_device(room["id"], device)
        self.assertCountEqual(self.repo.get_devices_in_room(room["id"]), devices)
        with self.assertRaises(RoomNotFoundError):
            self.repo.get_devices_in_room("non-existent-room")

    def test_add_user(self):
        user = {"id": "johndoe", "name": "John Doe"}
        self.assertEqual(self.repo.add_user(user), user)
        with self.assertRaises(UserAlreadyExistsError):
            self.repo.add_user(user)

    def test_get_user(self):
        with self.assertRaises(UserNotFoundError):
            self.repo.get_user("non-existent-user")
        user = {"id": "johndoe", "name": "John Doe"}
        self.repo.add_user(user)
        self.assertEqual(self.repo.get_user("johndoe"), user)

    def test_set_user_preferences(self):
        user = {"id": "johndoe", "name": "John Doe"}
        self.repo.add_user(user)
        preferences = {"language": "en", "theme": "dark"}
        self.repo.set_user_preferences(user["id"], preferences)
        self.assertEqual(self.repo.get_user(user["id"])["preferences"], preferences)
        with self.assertRaises(UserNotFoundError):
            self.repo.set_user_preferences("non-existent-user", preferences)

    def test_add_user_to_room(self):
        room = {"id": "1", "name": "Bedroom"}
        self.assertEqual(self.repo.add_room(room), room)
        user = {"id": "1", "name": "John Doe"}
        self.assertEqual(self.repo.add_user(user), user)
        self.repo.add_user_to_room(user["id"], room["id"])
        self.assertCountEqual(self.repo.get_users_in_room(room["id"]), [user])
        with self.assertRaises(UserNotFoundError):
            self.repo.add_user_to_room("non-existent-user", room["id"])
        with self.assertRaises(RoomNotFoundError):
            self.repo.add_user_to_room(user["id"], "non-existent-room")

    def test_get_users_in_room(self):
        room = {"id": "1", "name": "Bedroom"}
        self.repo.add_room(room)
        users = [
            {"id": "1", "name": "John Doe"},
            {"id": "2", "name": "Jane Doe"},
        ]
        for user in users:
            self.repo.add_user(user)
            self.repo.add_user_to_room(user["id"], room["id"])
        self.assertCountEqual(self.repo.get_users_in_room(room["id"]), users)
        with self.assertRaises(RoomNotFoundError):
            self.repo.get_users_in_room("non-existent-room")

    def test_remove_user_from_room(self):
        room = {"id": "1", "name": "Bedroom"}
        self.repo.add_room(room)
        user = {"id": "1", "name": "John Doe"}
        self.repo.add_user(user)
        self.repo.add_user_to_room(user["id"], room["id"])
        self.repo.remove_user_from_room(user["id"], room["id"])
        self.assertCountEqual(self.repo.get_users_in_room(room["id"]), [])
        with self.assertRaises(UserNotFoundError):
            self.repo.remove_user_from_room("non-existent-user", room["id"])
        with self.assertRaises(RoomNotFoundError):
            self.repo.remove_user_from_room(user["id"], "non-existent-room")


if __name__ == "__main__":
    unittest.main()
