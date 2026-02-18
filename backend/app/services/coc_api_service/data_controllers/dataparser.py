#import pandas as pd
#import numpy as np
#import arrow

from coc_api_service.events import EventEmitter, ClanDataParsedEvent, ErrorEvent

class DataParser(EventEmitter):
        #tag str # !
        #name str # !
        #badge Badge
        #level int # !
        #type str(open, inviteOnly or closed) # !
        #family_friendly bool # !
        #description str # !
        #location Location
        #points int # !
        #builder_base_points int # !
        #capital_points int # !
        #required_trophies int # !
        #required_builder_base_trophies int # !
        #required_townhall int # !
        #war_frequency str(always, etc) # !
        #war_win_streak int # !
        #war_wins int # !
        #war_ties int # !
        #war_losses int # !
        #public_war_log bool # !
        #member_count int # !
        #label_cls Label
        #member_cls ClanMember
        #capital_district_cls CapitalDistrict
        #war_league BaseLeague
        #capital_league BaseLeague
        #capital_districts List[CapitalDistrict]
        #labels List[Label]
        #members List[ClanMember]
        #members_dict Dict[str, ClanMember]
        # TODO CWwarlog, Raidwarlog, CWdata, CWLdata, Playerdata
    def __init__(self):
        super().__init__()
        print("DataParser.__init__(): успешная инициализация класса")

    async def parseClan(self, clan):
        try:
            clandata = {}

            clandata["tag"] = clan.tag
            clandata["name"] = clan.name
            clandata["level"] = clan.level
            clandata["type"] = clan.type
            clandata["family_friendly"] = clan.family_friendly
            clandata["description"] = clan.description
            #clandata["location"] = clan.location
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
            #clandata["label_cls"] = clan.label_cls
            #clandata["member_cls"] = clan.member_cls
            #clandata["capital_district_cls"] = clan.capital_district_cls
            #clandata["war_league"] = clan.war_league
            #clandata["capital_league"] = clan.capital_league
            #clandata["capital_districts"] = clan.capital_districts
            #clandata["labels"] = clan.labels
            #clandata["members"] = clan.members
            #clandata["members_dict"] = clan.members_dict

            await self.emit("clan_data_parsed", ClanDataParsedEvent(clandata))
            return clandata
        
        except Exception as e:
            error_msg = f"Ошибка при парсинге данных: {e}"
            print(f"DataParser.parseClan(): {error_msg}")
            await self.emit("error", ErrorEvent(error_msg))
            return None

