from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


class DatabaseRepository(ABC):
    @abstractmethod
    def add_room(self, room: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_room(self, room_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_rooms(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_device(self, room_id: str, device: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_devices_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def add_user_to_room(self, room_id: str, user_id: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_users_in_room(self, room_id: str) -> List[Dict[str, Any]]:
        pass