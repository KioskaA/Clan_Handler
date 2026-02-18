import coc
from coc_api_service.events import EventEmitter, ClanDataReceivedEvent, ErrorEvent


class DataCollector(EventEmitter):
    def __init__(self, clan_tag, login, password):
        super().__init__()
        self.cocAPIlogin = login
        self.cocAPIpassword = password
        self.ClanTag = clan_tag
        self.is_session = False

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
            error_msg = "Необходима авторизация"
            print(f"DataCollector.getClandata(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
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
            error_msg = f"Clah of Clans API находится в режиме обслуживания"
            print(f"DataCollector.getClandata(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None
        except coc.GatewayError:
            error_msg = f"Ошибка сети"
            print(f"DataCollector.getClandata(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
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
    #async def getClanMembersdata(self, clantag):  # ! (get_members → List[ClanMember]) Дает список участников клана
    #async def getRaidLog(self, clantag):          # ! (get_raid_log → RaidLog) Дает лог рейдов клана


    # ========== ЛИГА ВОЙН КЛАНОВ (ЛВК) ==========

    #async def getLeagueGroupdata(self, clantag):  # ! (get_league_group → ClanWarLeagueGroup) Дает группу ЛВК, в которой участвует выбранный клан
    #async def getLeagueWardata(self, wartag):     # ! (get_league_war → ClanWar) Дает данные о текущей ЛВК, war_tag является атрибутом coc.ClanWar


    # ========== ИГРОКИ ==========

    #async def getPlayerdata(self, player_tag):    # ! (get_player → Player) Дает подробные данные о игроке
    #async def getPlayersdata(self, player_tags):  # ! (get_players → AsyncIterator[Player]) Дает подробные данные о каждом игроке из списка


    async def close(self):
        if self.is_session:
            await self.client.close()
            print(f"DataCollector.close(): сессия успешно закрыта")
        else:
            print(f"DataCollector.close(): сессии не существует")