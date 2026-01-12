import asyncio
from collections import defaultdict
from typing import Any, Callable, Dict, List


class EventBus:
    """
    Basit pub/sub event bus. Modüller event'e abone olabilir ve event yayınlayabilir.
    """

    def __init__(self):
        self.subscribers: Dict[str, List[Callable[[Any], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, callback: Callable[[Any], None]):
        self.subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any):
        for callback in self.subscribers[event_type]:
            callback(data)


class AsyncMessageQueue:
    """
    Asenkron mesaj kuyruğu. Modüller arası mesajlaşma için kullanılır.
    """

    def __init__(self):
        self.queue = asyncio.Queue()

    async def send(self, message: Any):
        await self.queue.put(message)

    async def receive(self) -> Any:
        return await self.queue.get()
        return await self.queue.get()
        return await self.queue.get()
