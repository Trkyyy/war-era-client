"""Enumerations and literal types used by the WarEra API."""

from __future__ import annotations

import sys
from enum import Enum

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:

    class StrEnum(str, Enum):
        """Back-port of :class:`enum.StrEnum` for Python < 3.11."""

        def __str__(self) -> str:
            return self.value


# ── Event types ──────────────────────────────────────────────────────────────

class EventType(StrEnum):
    WAR_DECLARED = "warDeclared"
    PEACE_AGREEMENT = "peaceAgreement"
    BATTLE_OPENED = "battleOpened"
    BATTLE_ENDED = "battleEnded"
    NEW_PRESIDENT = "newPresident"
    REGION_TRANSFER = "regionTransfer"
    PEACE_MADE = "peaceMade"
    COUNTRY_MONEY_TRANSFER = "countryMoneyTransfer"
    DEPOSIT_DISCOVERED = "depositDiscovered"
    DEPOSIT_DEPLETED = "depositDepleted"
    SYSTEM_REVOLT = "systemRevolt"
    BANKRUPTCY = "bankruptcy"
    ALLIANCE_FORMED = "allianceFormed"
    ALLIANCE_BROKEN = "allianceBroken"
    REGION_LIBERATED = "regionLiberated"
    STRATEGIC_RESOURCES_RESHUFFLED = "strategicResourcesReshuffled"
    RESISTANCE_INCREASED = "resistanceIncreased"
    RESISTANCE_DECREASED = "resistanceDecreased"
    REVOLUTION_STARTED = "revolutionStarted"
    REVOLUTION_ENDED = "revolutionEnded"
    FINANCED_REVOLT = "financedRevolt"


# ── Battle helpers ───────────────────────────────────────────────────────────

class BattleDirection(StrEnum):
    FORWARD = "forward"
    BACKWARD = "backward"


class BattleFilter(StrEnum):
    ALL = "all"
    YOUR_COUNTRY = "yourCountry"
    YOUR_ENEMIES = "yourEnemies"


class BattleRankingDataType(StrEnum):
    DAMAGE = "damage"
    POINTS = "points"
    MONEY = "money"


class BattleRankingType(StrEnum):
    USER = "user"
    COUNTRY = "country"
    MU = "mu"


class BattleRankingSide(StrEnum):
    ATTACKER = "attacker"
    DEFENDER = "defender"


# ── Rankings ─────────────────────────────────────────────────────────────────

class RankingType(StrEnum):
    WEEKLY_COUNTRY_DAMAGES = "weeklyCountryDamages"
    WEEKLY_COUNTRY_DAMAGES_PER_CITIZEN = "weeklyCountryDamagesPerCitizen"
    COUNTRY_REGION_DIFF = "countryRegionDiff"
    COUNTRY_DEVELOPMENT = "countryDevelopment"
    COUNTRY_ACTIVE_POPULATION = "countryActivePopulation"
    COUNTRY_DAMAGES = "countryDamages"
    COUNTRY_WEALTH = "countryWealth"
    COUNTRY_PRODUCTION_BONUS = "countryProductionBonus"
    COUNTRY_BOUNTY = "countryBounty"
    WEEKLY_USER_DAMAGES = "weeklyUserDamages"
    USER_DAMAGES = "userDamages"
    USER_WEALTH = "userWealth"
    USER_LEVEL = "userLevel"
    USER_REFERRALS = "userReferrals"
    USER_SUBSCRIBERS = "userSubscribers"
    USER_TERRAIN = "userTerrain"
    USER_PREMIUM_MONTHS = "userPremiumMonths"
    USER_PREMIUM_GIFTS = "userPremiumGifts"
    USER_CASES_OPENED = "userCasesOpened"
    USER_GEMS_PURCHASED = "userGemsPurchased"
    USER_BOUNTY = "userBounty"
    MU_WEEKLY_DAMAGES = "muWeeklyDamages"
    MU_DAMAGES = "muDamages"
    MU_TERRAIN = "muTerrain"
    MU_WEALTH = "muWealth"
    MU_BOUNTY = "muBounty"


# ── Articles ─────────────────────────────────────────────────────────────────

class ArticleListType(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    TOP = "top"
    MY = "my"
    SUBSCRIPTIONS = "subscriptions"
    LAST = "last"


# ── Transactions ─────────────────────────────────────────────────────────────

class TransactionType(StrEnum):
    APPLICATION_FEE = "applicationFee"
    TRADING = "trading"
    ITEM_MARKET = "itemMarket"
    WAGE = "wage"
    DONATION = "donation"
    ARTICLE_TIP = "articleTip"
    OPEN_CASE = "openCase"
    CRAFT_ITEM = "craftItem"
    DISMANTLE_ITEM = "dismantleItem"


# ── Upgrades ─────────────────────────────────────────────────────────────────

class UpgradeType(StrEnum):
    BUNKER = "bunker"
    BASE = "base"
    PACIFICATION_CENTER = "pacificationCenter"
    STORAGE = "storage"
    AUTOMATED_ENGINE = "automatedEngine"
    BREAK_ROOM = "breakRoom"
    HEADQUARTERS = "headquarters"
    DORMITORIES = "dormitories"
