import coc
from coc_api_service.events import EventEmitter, ClanDataReceivedEvent, ErrorEvent, ClanMembersDataReceivedEvent


class DataCollector(EventEmitter):
    def __init__(self, clan_tag, login, password):
        super().__init__()
        self.cocAPIlogin = login
        self.cocAPIpassword = password
        self.ClanTag = clan_tag
        self.is_session = False
        self.error_msges = (
            "Необходима авторизация",
            "Clah of Clans API находится в режиме обслуживания",
            "Ошибка сети"
        )

        print(f"DataCollector.__init__(): успешная инициализация класса")

    async def logIn(self):
        if not self.is_session:
            self.client = coc.Client()
            try:
                await self.client.login(self.cocAPIlogin, self.cocAPIpassword)
                self.is_session = True
                print(f"DataCallector.login(): авторизация прошла успешно")
            except coc.InvalidCredentials as error:
                print(f"DataCollector.login(): ошибка авторизации: {error}")
                raise
        else:
            print("Сессия уже существует")

    async def getClandata(self):
        if not self.is_session:
            print(f"DataCollector.getClandata(): {self.error_msges[0]}")
            await self.emit("error", ErrorEvent(self.error_msges[0]))
            return None
        try:
            data = await self.client.get_clan(self.ClanTag)
            print(f"DataCollector.getСlandata(): данные о клане {data.name} {data.tag} получены")
            await self.emit("clan_data_received", ClanDataReceivedEvent(data))
            return data
        except coc.NotFound:
            error_msg = f"Клана с тегом {self.ClanTag} не существует"
            print(f"DataCollector.getClandata(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None
        except coc.Maintenance:
            print(f"DataCollector.getClandata(): {self.error_msges[1]}")
            await self.emit("error", ErrorEvent(self.error_msges[1]))
            return None
        except coc.GatewayError:
            print(f"DataCollector.getClandata(): {self.error_msges[2]}")
            await self.emit("error", ErrorEvent(self.error_msges[2]))
            return None

    async def getClanMembersdata(self, clantag):  # ! (get_players → AsyncIterator[Player]) Дает подробные данные о каждом игроке из списка
        if not self.is_session:
            print(f"DataCollector.getClanMembersdata(): {self.error_msges[0]}")
            await self.emit("error", ErrorEvent(self.error_msges[0]))
            return None
        try:
            members = await self.client.get_members(clantag)

            tags = []
            for member in members:
                tags.append(str(member.tag))

            data = self.client.get_players(tags)
            print(f"DataCollector.getClanMembersdata(): данные об участниках клана {clantag} получены")
            await self.emit("clan_members_data_received", ClanMembersDataReceivedEvent(data))
            return data
        except coc.NotFound:
            error_msg = f"Клана с тегом {clantag} не существует"
            print(f"DataCollector.getClanMembersdata(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None
        except coc.Maintenance:
            print(f"DataCollector.getClanMembersdata(): {self.error_msges[1]}")
            await self.emit("error", ErrorEvent(self.error_msges[1]))
            return None
        except coc.GatewayError:
            print(f"DataCollector.getClanMembersdata(): {self.error_msges[2]}")
            await self.emit("error", ErrorEvent(self.error_msges[2]))
            return None

    # ========== ПОИСК ВСЕХ (СПИСКИ) ==========

    #async def getLeaguesdata(self):           # ! (search_leagues → List[League]) Дает список(ID, название, иконка) всех лиг
    #async def getWarLeaguesdata(self):        # ! (search_war_leagues → List[BaseLeague]) Дает список(ID, название) всех лиг КВ
    #async def getBBLeaguesdata(self):         # ! (search_builder_base_leagues → List[BaseLeague]) Дает список(ID, название) всех лиг деревни строителей
    #async def getCapitalLeaguesdata(self):    # ! (search_capital_leagues → List[BaseLeague]) Дает список(ID, название) всех лиг столицы


    # ========== ПОЛУЧЕНИЕ КОНКРЕТНОГО ЭЛЕМЕНТА ==========

    #async def getLeaguedata(self, league_name):      # ! (get_league → List[League]) Дает название, ID и иконку лиги
    #async def getWarLeaguedata(self, league_id):     # ! (get_war_league → List[BaseLeague]) Дает название и ID ЛВК
    #async def getBBLeaguedata(self, league_id):      # ! (get_builder_base_league → List[BaseLeague]) Дает название и ID лиги деревни строителя
    #async def getCapitalLeaguedata(self, league_id): # ! (get_capital_league → List[BaseLeague]) Дает название и ID лиги столицы


    # ========== КЛАН И ВОЙНЫ ==========

    #async def getClanWardata(self, clantag):      # ! (get_clan_war → ClanWar) Дает данные о текущей КВ клана
    #async def getCurrentWardata(self, clantag):   # ! (get_current_war → ClanWar | None) Дает данные о текущей КВ клана (можно сделать проверку на ЛВК)
    #async def getWarLog(self, clantag):           # ! (get_war_log → ClanWarLog) Дает лог КВ
    #async def getRaidLog(self, clantag):          # ! (get_raid_log → RaidLog) Дает лог рейдов клана


    # ========== ЛИГА ВОЙН КЛАНОВ (ЛВК) ==========

    #async def getLeagueGroupdata(self, clantag):  # ! (get_league_group → ClanWarLeagueGroup) Дает группу ЛВК, в которой участвует выбранный клан
    #async def getLeagueWardata(self, wartag):     # ! (get_league_war → ClanWar) Дает данные о текущей ЛВК, war_tag является атрибутом coc.ClanWar



    async def close(self):
        if self.is_session:
            await self.client.close()
            print(f"DataCollector.close(): сессия успешно закрыта")
        else:
            print(f"DataCollector.close(): сессии не существует")