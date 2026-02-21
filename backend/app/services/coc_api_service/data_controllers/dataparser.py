from coc_api_service.events import EventEmitter, ClanDataParsedEvent, ClanMembersDataParsedEvent, ErrorEvent

class DataParser(EventEmitter):
        # TODO CWwarlog, Raidwarlog, CWdata, CWLdata, Playerdata
    def __init__(self):
        super().__init__()
        print("DataParser.__init__(): успешная инициализация класса")

    async def parseClan(self, clan):
        print(f"DataParser.parseClan(): Запуск парсинга клана")
        try:
            clandata = {}

            clandata["tag"] = clan.tag
            clandata["name"] = clan.name
            clandata["badge"] = clan.badge.large
            clandata["level"] = clan.level
            clandata["type"] = clan.type
            clandata["family_friendly"] = clan.family_friendly
            clandata["description"] = clan.description
            clandata["location"] = clan.location.name
            clandata["points"] = clan.points
            clandata["builder_base_points"] = clan.builder_base_points
            clandata["capital_points"] = clan.capital_points
            clandata["required_trophies"] = clan.required_trophies
            clandata["required_builder_base_trophies"] = clan.required_builder_base_trophies
            clandata["required_townhall"] = clan.required_townhall
            clandata["war_frequency"] = clan.war_frequency
            clandata["war_win_streak"] = clan.war_win_streak
            clandata["war_wins"] = clan.war_wins
            clandata["war_ties"] = clan.war_ties
            clandata["war_losses"] = clan.war_losses
            clandata["public_war_log"] = clan.public_war_log
            clandata["member_count"] = clan.member_count
            clandata["labels"] = [(label.name, label.badge.medium) for label in clan.labels]
            clandata["members"] = [(member.tag) for member in clan.members]
            clandata["war_league"] = clan.war_league.name
            clandata["capital_league"] = clan.capital_league.name
            clandata["capital_districts"] = [(district.name, district.hall_level) for district in clan.capital_districts]

            await self.emit("clan_data_parsed", ClanDataParsedEvent(clandata))
            print(f"DataParser.parseClan(): данные клана обработаны")
            return clandata
        
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseClan(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None
        
    async def parseClanMembers(self, memberslist):
        print(f"DataParser.parseClanMembers(): Запуск парсинга списка участников клана")
        try:
            members = []
            async for member in memberslist:
                members.append({
                    "tag": member.tag,
                    "name": member.name,
                    "role": member.role,
                    "town_hall": member.town_hall,
                    "donations": member.donations
                })

            await self.emit("clan_members_data_parsed", ClanMembersDataParsedEvent(members))
            print(f"DataParser.parseClanMembers(): список участников клана обработан")
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseClan(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None
