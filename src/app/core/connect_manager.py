from uuid import UUID

from fastapi import WebSocket

from src.app.core.exceptions import NotFoundException


class ConnectManager:
    def __init__(self):
        self.pool: dict[UUID, WebSocket] = {}

    async def connect(self, user_id: UUID, websocket: WebSocket):
        await websocket.accept()
        self.pool[user_id] = websocket

    def disconnect(self, user_id: UUID):
        if self.pool[user_id]:
            del self.pool[user_id]

    async def send_message(self, user_id: UUID, msg: dict[str, str]):
        if user_id not in self.pool:
            raise NotFoundException(f'Не найдено активного соединения с user_id={user_id}')
        await self.pool[user_id].send_text("Что нибудь))")
