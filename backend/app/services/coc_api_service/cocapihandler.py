import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_controllers.datacollector import DataCollector
from data_controllers.dataparser import DataParser
from coc_api_service.events import EventEmitter, ClanDataReceivedEvent, ClanDataParsedEvent, ErrorEvent


load_dotenv()
LOGIN = os.getenv("cocapilogin")
PASSWORD = os.getenv("cocapipassword")
CLANTAG = "#2CY9RP90Q"

class CoCAPIHandler(EventEmitter):
    def __init__(self, clantag, login, password):
        super().__init__()
        self.clantag = clantag
        self.login = login
        self.password = password

        print(f"CoCAPIHandler.__init__(): Успешная инициализация")

        self.data_parser = DataParser()
        self.data_collector = DataCollector(clantag, login, password)

        self._setup_event_handlers()

    def _setup_event_handlers(self):
        async def handle_clan_data_received(event: ClanDataReceivedEvent):
            print("CoCAPIHandler: Получены данные клана, начинаю парсинг")
            await self.data_parser.parseClan(event.data)
        
        self.data_collector.on("clan_data_received", handle_clan_data_received)
        
        async def handle_clan_data_parsed(event: ClanDataParsedEvent):
            print("CoCAPIHandler: Данные клана распарсены")
            await self.emit("clan_data_ready", event)
        
        self.data_parser.on("clan_data_parsed", handle_clan_data_parsed)
        
        async def handle_collector_error(event: ErrorEvent):
            print(f"CoCAPIHandler: Получена ошибка от коллектора: {event.data}")
            await self.emit("error", event)
        
        async def handle_parser_error(event: ErrorEvent):
            print(f"CoCAPIHandler: Получена ошибка от парсера: {event.data}")
            await self.emit("error", event)
        
        self.data_collector.on("error", handle_collector_error)
        self.data_parser.on("error", handle_parser_error)

    async def logIn(self):
        """Авторизация"""
        await self.data_collector.logIn()
        print(f"CoCAPIHandler.login(): Успешная авторизация")

    async def fetch_clan_data(self):
        """Запрос данных клана (запускает цепочку событий)"""
        print("CoCAPIHandler: Запрашиваю данные клана")
        await self.data_collector.getClandata()

    async def close(self):
        """Закрытие соединения"""
        await self.data_collector.close()
        print(f"CoCAPIHandler.close(): сессия успешно закрыта")


def printfromDict(Dict, name="Dict"):
    """Вспомогательная функция для печати словаря"""
    print(f"\n--- {name} ---")
    for key, value in Dict.items():
        print(f"{key}: {value}")
    print("---" + "-" * len(name) + "---")


async def main():
    # Создаем обработчик
    handler = CoCAPIHandler(CLANTAG, LOGIN, PASSWORD)
    
    # Подписываемся на события
    async def on_clan_data_ready(event: ClanDataParsedEvent):
        print("\n🎯 Получены готовые данные клана!")
        printfromDict(event.data, "Clan Data")
    
    handler.on("clan_data_ready", on_clan_data_ready)
    
    async def on_error(event: ErrorEvent):
        print(f"\n❌ Ошибка: {event.data}")
    
    handler.on("error", on_error)
    
    try:
        # Авторизуемся
        await handler.logIn()
        
        # Запрашиваем данные (всё остальное произойдет через события)
        await handler.fetch_clan_data()
        
        # Даем время на обработку событий
        await asyncio.sleep(2)
        
    finally:
        await handler.close()

if __name__ == "__main__":
    asyncio.run(main())