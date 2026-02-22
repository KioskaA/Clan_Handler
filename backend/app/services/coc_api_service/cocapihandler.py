import asyncio
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from data_controllers.datacollector import DataCollector
from data_controllers.dataparser import DataParser
from coc_api_service.events import (
                                    EventEmitter,
                                    ClanDataReceivedEvent, ClanDataParsedEvent,
                                    ClanMembersDataReceivedEvent, ClanMembersDataParsedEvent,
                                    ClanRaidLogReceivedEvent, ClanRaidlogParsedEvent,
                                    ErrorEvent
                                )


load_dotenv()
LOGIN = os.getenv("cocapilogin")
PASSWORD = os.getenv("cocapipassword")
CLANTAG = "#2CY9RP90Q" # * Elements
#CLANTAG = "#2YYVLLGR" # * AintSoSerious

class CoCAPIHandler(EventEmitter):
    def __init__(self, login, password):
        super().__init__()
        self.login = login
        self.password = password

        print(f"CoCAPIHandler.__init__(): Успешная инициализация")

        self.data_parser = DataParser()
        self.data_collector = DataCollector(login, password)

        self._setup_event_handlers()

    def _setup_event_handlers(self):
        # *---* Данные клана *---* 
        async def handle_clan_data_received(event: ClanDataReceivedEvent):
            print("CoCAPIHandler: Получены данные клана, начинаю парсинг")
            await self.data_parser.parseClan(event.data)
        
        self.data_collector.on("clan_data_received", handle_clan_data_received)
        
        async def handle_clan_data_parsed(event: ClanDataParsedEvent):
            print("CoCAPIHandler: Данные клана распарсены")
            await self.emit("clan_data_ready", event)
        
        self.data_parser.on("clan_data_parsed", handle_clan_data_parsed)

        # *---* Данные об участниках клана *---*
        async def handle_clan_members_data_received(event: ClanMembersDataReceivedEvent):
            print("CoCAPIHandler: Получен список участников клана, начинаю парсинг")
            await self.data_parser.parseClanMembers(event.data)

        self.data_collector.on("clan_members_data_received", handle_clan_members_data_received)

        async def handle_clan_members_data_parsed(event: ClanMembersDataParsedEvent):
            print("CoCAPIHandler: Список участников клана распарсен")
            await self.emit("clan_members_data_ready", event)

        self.data_parser.on("clan_members_data_parsed", handle_clan_members_data_parsed)
        
        # *---* Рейдлог *---*
        async def handle_clan_raidlog_received(event: ClanRaidLogReceivedEvent):
            print("CoCAPIHandler: Получен рейдлог клана, начинаю парсинг")
            await self.data_parser.parseRaidLog(event.data)

        self.data_collector.on("clan_raidlog_received", handle_clan_raidlog_received)

        async def handle_clan_raidlog_parsed(event: ClanRaidlogParsedEvent):
            print("CoCAPIHandler: Рейдлог клана распарсен")
            await self.emit("clan_raidlog_ready", event)

        self.data_parser.on("clan_raidlog_parsed", handle_clan_raidlog_parsed)

        # *---* Обработка ошибок коллектора *---*
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

    async def fetch_clan_data(self, clantag):
        """Запрос данных клана (запускает цепочку событий)"""
        print("CoCAPIHandler: Запрашиваю данные клана")
        await self.data_collector.getClandata(clantag)

    async def fetch_clan_members_data(self, clantag):
        print("CoCAPIHandler: Запрашиваю данные об участниках клана")
        await self.data_collector.getClanMembersdata(clantag)

    async def fetch_clan_raidlog(self, clantag, limit=5):
        print("CoCAPIHandler: Запрашиваю рейдлог клана")
        await self.data_collector.getRaidLog(clantag, limit=limit)

    async def close(self):
        """Закрытие соединения"""
        await self.data_collector.close()
        print(f"CoCAPIHandler.close(): сессия успешно закрыта")


def printfromDict(Dict, name="Dict", showname = True):
    if showname:
        print(f"\n--- {name} ---")
        for key, value in Dict.items():
            print(f"{key}: {value}")
        print("---" + "-" * len(name) + "---")
    elif not showname:
        for key, value in Dict.items():
            print(f"{key}: {value}")

def printfromList(List, name="List", amount: str | int = "full", showname = True):
    if amount != "full":
        if not isinstance(amount, (int, float)):
            print(f"CoCAPIHandler.printfromList(): Параметр amount должен быть 'full' или числом, получено: {amount}")
            return None
        amount = int(amount)
        if amount <= 0:
            print(f"CoCAPIHandler.printfromList(): Параметр amount должен быть положительным числом, получено: {amount}")
            return None
        if amount > len(List):
            print(f"CoCAPIHandler.printfromList(): Параметр amount ({amount}) превышает длину списка ({len(List)})")
            return None
    if showname:
        print(f"\n--- {name} ---")
    items_to_print = List if amount == "full" else List[:amount]
    for item in items_to_print:
        printfromDict(item, showname=False)
        print("---" + "-" * len(name) + "---")


    #if amount > len(List):
    #    print(f"CoCAPIHandler.printfromList(): Параметр amount должен быть <= длины списка или 'full', получено: {amount}")
    #    return None
    #if showname:
    #    print(f"\n--- {name} ---")
    #
    #if amount == "full":
    #    for item in List:
    #        printfromDict(item, showname=False)
    #        print("---" + "-" * len(name) + "---")
    #else:
    #    i = 0
    #    while i <= int(amount):
    #        for item in List:
    #            printfromDict(item, showname=False)
    #            print("---" + "-" * len(name) + "---")
    #            i += 1

async def main():
    # Создаем обработчик
    handler = CoCAPIHandler(LOGIN, PASSWORD)
    
    # Подписываемся на события
    async def on_clan_data_ready(event: ClanDataParsedEvent):
        print("\n🎯 Получены готовые данные клана!")
        printfromDict(event.data, "Clan Data")
    
    handler.on("clan_data_ready", on_clan_data_ready)
    
    async def on_clan_members_data_ready(event: ClanMembersDataParsedEvent, amount="full"):
        print(f"\n🎯 Получены готовые данные об {len(event.data)} участниках клана!")
        if amount == "full":
            printfromList(event.data, "Clan members Data")
        else:
            printfromList(event.data, "Clan members Data", amount=amount)

    handler.on("clan_members_data_ready", lambda event: on_clan_members_data_ready(event, amount=1)) # ! <<<<< МЕНЯТЬ КОЛИЧЕСТВО ВЫВОДИМЫХ УЧАСТНИКОВ КЛАНА ЗДЕСЬ!!!!

    async def on_clan_raidlog_ready(event:ClanRaidlogParsedEvent):
        print(f"\n🎯 Получен готовый рейдлог клана!")
        printfromList(event.data, "Raidlog")

    handler.on("clan_raidlog_ready", on_clan_raidlog_ready)

    async def on_error(event: ErrorEvent):
        print(f"\n❌ Ошибка: {event.data}")
    
    handler.on("error", on_error)
    
    try:
        await handler.logIn()
        
        # Запрашиваем данные
        #await handler.fetch_clan_data(clantag=CLANTAG)
        await handler.fetch_clan_members_data(clantag=CLANTAG)
        #await handler.fetch_clan_raidlog(clantag=CLANTAG, limit=1)
        
        await asyncio.sleep(2)
        
    finally:
        await handler.close()

if __name__ == "__main__":
    asyncio.run(main())