# events.py
from typing import Dict, Any, Callable, Awaitable
import asyncio

class Event:
    def __init__(self, data: Any = None):
        self.data = data

class ClanDataReceivedEvent(Event):
    pass

class ClanDataParsedEvent(Event):
    pass

class ClanMembersDataReceivedEvent(Event):
    pass

class ClanMembersDataParsedEvent(Event):
    pass

class ErrorEvent(Event):
    pass

class EventEmitter:
    def __init__(self):
        self._listeners: Dict[str, list] = {}

    def on(self, event_name: str, callback: Callable[[Event], Awaitable[None]]):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)
        print(f"EventEmitter.on(): Подписка на событие {event_name}")

    async def emit(self, event_name: str, event: Event):
        if event_name in self._listeners:
            print(f"EventEmitter.emit(): Отправка события {event_name}")
            for callback in self._listeners[event_name]:
                try:
                    await callback(event)
                except Exception as e:
                    print(f"Ошибка в обработчике события {event_name}: {e}")