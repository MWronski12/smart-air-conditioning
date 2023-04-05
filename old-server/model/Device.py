from uuid import UUID


class Device:
    def __init__(self, room_id: UUID, device_id: int) -> None:
        self.room_id = room_id
        self.device_id = device_id

    def __hash__(self) -> int:
        return hash((self.device_id, self.room_id))
