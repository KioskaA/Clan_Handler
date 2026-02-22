from coc_api_service.events import EventEmitter, ClanDataParsedEvent, ClanMembersDataParsedEvent, ClanRaidlogParsedEvent, ClanWarLogParsedEvent, ErrorEvent

class DataParser(EventEmitter):
        # TODO CWwarlog, CWdata, CWLdata
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
            clandata["labels"] = [(label.name) for label in clan.labels]
            clandata["members"] = [(member.tag) for member in clan.members]
            clandata["war_league"] = clan.war_league.name
            clandata["capital_league"] = clan.capital_league.name
            clandata["capital_districts"] = [{"name": district.name, "hall_level": district.hall_level} for district in clan.capital_districts]

            await self.emit("clan_data_parsed", ClanDataParsedEvent(clandata))
            print(f"DataParser.parseClan(): данные клана обработаны")
            return clandata
        
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseClan(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None


    async def parseClanMembers(self, memberslist):

        async def parseAchievementlist(achievementlist):
            achievements = []
            for achievement in achievementlist:
                achievements.append({
                    "name": achievement.name,
                    "stars": achievement.stars,
                    "value": achievement.value,
                    "target": achievement.target,
                    # "village": str(achievement.village), # str: Either home or builderBase # Хз, возможно понадобится когда-нибудь
                })
            return achievements
        
        async def parseTroopslist(trooplist):
            if not trooplist:
                return []
            
            troops = []
            for troop in trooplist:
                troops.append({
                    "name": troop.name,
                    "level": troop.level,
                })
            return troops
        
        def parse_season(season_obj):
            if season_obj is None:
                return None
            return {
                "id": season_obj.id if hasattr(season_obj, 'id') else None,
                "trophies": season_obj.trophies if hasattr(season_obj, 'trophies') else None,
                "rank": season_obj.rank if hasattr(season_obj, 'rank') else None
            }
        
        async def parseLegendStatistics(legend_statistics):
            if legend_statistics == None:
                return None
            else:
                legstat = {
                    "legend_trophies": getattr(legend_statistics, 'legend_trophies', 0),
                    "current_season": parse_season(getattr(legend_statistics, 'current_season', None)),
                    "previous_season": parse_season(getattr(legend_statistics, 'previous_season', None)),
                    "best_season": parse_season(getattr(legend_statistics, 'best_season', None)),
                    "previous_builder_base_season": parse_season(getattr(legend_statistics, 'previous_builder_base_season', None)),
                    "best_builder_base_season": parse_season(getattr(legend_statistics, 'best_builder_base_season', None)),
                }
                return legstat

        print(f"DataParser.parseClanMembers(): Запуск парсинга списка участников клана")
        try:
            members = []
            async for member in memberslist:
                members.append({
                    "tag": member.tag,
                    "name": member.name,
                    "role": member.role.in_game_name,
                    "town_hall": member.town_hall,
                    "exp_level": member.exp_level,
                    "league": member.league.name,
                    "builder_base_league": member.builder_base_league.name,
                    "trophies": member.trophies,
                    "builder_base_trophies": member.builder_base_trophies,
                    "clan_rank": member.clan_rank,
                    "clan_previous_rank": member.clan_previous_rank,
                    "builder_base_rank": member.builder_base_rank,
                    "donations": member.donations,
                    "received": member.received,
                    "attack_wins": member.attack_wins,
                    "defense_wins": member.defense_wins,
                    "best_trophies": member.best_trophies,
                    "war_stars": member.war_stars,
                    "town_hall_weapon": member.town_hall_weapon,
                    "builder_hall": member.builder_hall,
                    "best_builder_base_trophies": member.best_builder_base_trophies,
                    "clan_capital_contributions": member.clan_capital_contributions,
                    "legend_statistics": await parseLegendStatistics(member.legend_statistics),
                    "war_opted_in": member.war_opted_in,
                    "achievements": await parseAchievementlist(member.achievements),
                    "builder_troops": await parseTroopslist(member.builder_troops),
                    "home_troops": await parseTroopslist(member.home_troops),
                    "super_troops": await parseTroopslist(member.super_troops),
                    "siege_machines": await parseTroopslist(member.siege_machines),
                    "spells": await parseTroopslist(member.spells),
                    "labels": [(label.name) for label in member.labels],
                    "equipment": await parseTroopslist(member.equipment),
                    "heroes": await parseTroopslist(member.heroes),
                    "pets": await parseTroopslist(member.pets),
                })
            await self.emit("clan_members_data_parsed", ClanMembersDataParsedEvent(members))
            print(f"DataParser.parseClanMembers(): список участников клана обработан")
            return members
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseClanMembers(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None


    async def parseRaidLog(self, raidlog):

        async def parse_RaidMembers(memberslist):
            raidmembers = []
            for member in memberslist:
                raidmembers.append({
                    "tag": member.tag,
                    "name": member.name,
                    "attack_count": member.attack_count,
                    "attack_limit": member.attack_limit,
                    "bonus_attack_limit": member.bonus_attack_limit,
                    "capital_resources_looted": member.capital_resources_looted,
                    #"attacks": member.attacks,
                    "attacks": "Будет добавлено после кв", # TODO <<<<<<<
                })
            return raidmembers

        print(f"DataParser.parseRaidLog(): Запуск парсинга рейдлога клана")
        try:
            logs = []
            for log in raidlog:
                logs.append({
                    "state": log.state,
                    "start_time": log.start_time.now,
                    "end_time": log.end_time.now,
                    "total_loot": log.total_loot,
                    "completed_raid_count": log.completed_raid_count,
                    "attack_count": log.attack_count,
                    "destroyed_district_count": log.destroyed_district_count,
                    "offensive_reward": log.offensive_reward,
                    "defensive_reward": log.defensive_reward,
                    "defense_attack_count": log.defense_attack_count,
                    "defensive_destroyed_district_count": log.defensive_destroyed_district_count,
                    "total_defensive_loot": log.total_defensive_loot,
                    "members": await parse_RaidMembers(log.members),
                    #"attack_log": log.attack_log,
                    "attack_log": "Будет добавлено после кв", # TODO <<<<<<<
                    #"defense_log": log.defense_log,
                    "defense_log": "Будет добавлено после кв", # TODO <<<<<<<
                })
            await self.emit("clan_raidlog_parsed", ClanRaidlogParsedEvent(logs))
            print(f"DataParser.parseRaidLog(): Рейдлог клана обработан")
            return logs
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseRaidLog(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None

    async def parseWarLog(self, warlog, type="cw"):
        print(f"DataParser.parseWarLog(): Запуск парсинга варлога клана")
        try:
            cwlogs = []
            cwllogs = []
            for log in warlog:
                if not log.is_league_entry:
                    cwlogs.append({
                        "result": log.result,
                        "end_time": log.end_time.now,
                        "team_size": log.team_size,
                        "clan": log.clan, # TODO <<<<<<<
                        "opponent": log.opponent, # TODO <<<<<<<
                        "attacks_per_member": log.attacks_per_member,
                        "battle_modifier": log.battle_modifier,
                        "is_league_entry": log.is_league_entry,
                    })
                else:
                    cwllogs.append({
                        "result": log.result,
                        "end_time": log.end_time.now,
                        "team_size": log.team_size,
                        "clan": log.clan, # TODO <<<<<<<
                        "opponent": log.opponent, # TODO <<<<<<<
                        "attacks_per_member": log.attacks_per_member,
                        "battle_modifier": log.battle_modifier,
                        "is_league_entry": log.is_league_entry,
                    })
            
            if type == "cw":
                logs = cwlogs
                await self.emit("clan_warlog_parsed", ClanWarLogParsedEvent(logs, type=type))
            elif type == "cwl":
                logs = cwllogs
                await self.emit("clan_warlog_parsed", ClanWarLogParsedEvent(logs, type=type))
            else:
                print(f"DataParser.parseWarLog(): Параметр type некорректен: {type}")
                return None

            print(f"DataParser.parseWarLog(): Рейдлог клана обработан")
            return logs
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseWarLog(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None