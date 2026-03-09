"""Tests for the warera.enums module.

Verifies every enum has the expected members and string values.
"""

from __future__ import annotations

import pytest

from warera.enums import (
    ArticleListType,
    BattleDirection,
    BattleFilter,
    BattleRankingDataType,
    BattleRankingSide,
    BattleRankingType,
    EventType,
    RankingType,
    TransactionType,
    UpgradeType,
)


class TestEventType:
    def test_member_count(self):
        assert len(EventType) == 21

    @pytest.mark.parametrize(
        "member, value",
        [
            (EventType.WAR_DECLARED, "warDeclared"),
            (EventType.PEACE_AGREEMENT, "peaceAgreement"),
            (EventType.BATTLE_OPENED, "battleOpened"),
            (EventType.BATTLE_ENDED, "battleEnded"),
            (EventType.NEW_PRESIDENT, "newPresident"),
            (EventType.REGION_TRANSFER, "regionTransfer"),
            (EventType.PEACE_MADE, "peaceMade"),
            (EventType.COUNTRY_MONEY_TRANSFER, "countryMoneyTransfer"),
            (EventType.DEPOSIT_DISCOVERED, "depositDiscovered"),
            (EventType.DEPOSIT_DEPLETED, "depositDepleted"),
            (EventType.SYSTEM_REVOLT, "systemRevolt"),
            (EventType.BANKRUPTCY, "bankruptcy"),
            (EventType.ALLIANCE_FORMED, "allianceFormed"),
            (EventType.ALLIANCE_BROKEN, "allianceBroken"),
            (EventType.REGION_LIBERATED, "regionLiberated"),
            (EventType.STRATEGIC_RESOURCES_RESHUFFLED, "strategicResourcesReshuffled"),
            (EventType.RESISTANCE_INCREASED, "resistanceIncreased"),
            (EventType.RESISTANCE_DECREASED, "resistanceDecreased"),
            (EventType.REVOLUTION_STARTED, "revolutionStarted"),
            (EventType.REVOLUTION_ENDED, "revolutionEnded"),
            (EventType.FINANCED_REVOLT, "financedRevolt"),
        ],
    )
    def test_values(self, member, value):
        assert member == value
        assert str(member) == value


class TestBattleDirection:
    def test_member_count(self):
        assert len(BattleDirection) == 2

    def test_forward(self):
        assert BattleDirection.FORWARD == "forward"

    def test_backward(self):
        assert BattleDirection.BACKWARD == "backward"


class TestBattleFilter:
    def test_member_count(self):
        assert len(BattleFilter) == 3

    @pytest.mark.parametrize(
        "member, value",
        [
            (BattleFilter.ALL, "all"),
            (BattleFilter.YOUR_COUNTRY, "yourCountry"),
            (BattleFilter.YOUR_ENEMIES, "yourEnemies"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestBattleRankingDataType:
    def test_member_count(self):
        assert len(BattleRankingDataType) == 3

    @pytest.mark.parametrize(
        "member, value",
        [
            (BattleRankingDataType.DAMAGE, "damage"),
            (BattleRankingDataType.POINTS, "points"),
            (BattleRankingDataType.MONEY, "money"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestBattleRankingType:
    def test_member_count(self):
        assert len(BattleRankingType) == 3

    @pytest.mark.parametrize(
        "member, value",
        [
            (BattleRankingType.USER, "user"),
            (BattleRankingType.COUNTRY, "country"),
            (BattleRankingType.MU, "mu"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestBattleRankingSide:
    def test_member_count(self):
        assert len(BattleRankingSide) == 2

    def test_attacker(self):
        assert BattleRankingSide.ATTACKER == "attacker"

    def test_defender(self):
        assert BattleRankingSide.DEFENDER == "defender"


class TestRankingType:
    def test_member_count(self):
        assert len(RankingType) == 26

    @pytest.mark.parametrize(
        "member, value",
        [
            (RankingType.WEEKLY_COUNTRY_DAMAGES, "weeklyCountryDamages"),
            (RankingType.WEEKLY_COUNTRY_DAMAGES_PER_CITIZEN, "weeklyCountryDamagesPerCitizen"),
            (RankingType.COUNTRY_REGION_DIFF, "countryRegionDiff"),
            (RankingType.COUNTRY_DEVELOPMENT, "countryDevelopment"),
            (RankingType.COUNTRY_ACTIVE_POPULATION, "countryActivePopulation"),
            (RankingType.COUNTRY_DAMAGES, "countryDamages"),
            (RankingType.COUNTRY_WEALTH, "countryWealth"),
            (RankingType.COUNTRY_PRODUCTION_BONUS, "countryProductionBonus"),
            (RankingType.COUNTRY_BOUNTY, "countryBounty"),
            (RankingType.WEEKLY_USER_DAMAGES, "weeklyUserDamages"),
            (RankingType.USER_DAMAGES, "userDamages"),
            (RankingType.USER_WEALTH, "userWealth"),
            (RankingType.USER_LEVEL, "userLevel"),
            (RankingType.USER_REFERRALS, "userReferrals"),
            (RankingType.USER_SUBSCRIBERS, "userSubscribers"),
            (RankingType.USER_TERRAIN, "userTerrain"),
            (RankingType.USER_PREMIUM_MONTHS, "userPremiumMonths"),
            (RankingType.USER_PREMIUM_GIFTS, "userPremiumGifts"),
            (RankingType.USER_CASES_OPENED, "userCasesOpened"),
            (RankingType.USER_GEMS_PURCHASED, "userGemsPurchased"),
            (RankingType.USER_BOUNTY, "userBounty"),
            (RankingType.MU_WEEKLY_DAMAGES, "muWeeklyDamages"),
            (RankingType.MU_DAMAGES, "muDamages"),
            (RankingType.MU_TERRAIN, "muTerrain"),
            (RankingType.MU_WEALTH, "muWealth"),
            (RankingType.MU_BOUNTY, "muBounty"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestArticleListType:
    def test_member_count(self):
        assert len(ArticleListType) == 6

    @pytest.mark.parametrize(
        "member, value",
        [
            (ArticleListType.DAILY, "daily"),
            (ArticleListType.WEEKLY, "weekly"),
            (ArticleListType.TOP, "top"),
            (ArticleListType.MY, "my"),
            (ArticleListType.SUBSCRIPTIONS, "subscriptions"),
            (ArticleListType.LAST, "last"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestTransactionType:
    def test_member_count(self):
        assert len(TransactionType) == 9

    @pytest.mark.parametrize(
        "member, value",
        [
            (TransactionType.APPLICATION_FEE, "applicationFee"),
            (TransactionType.TRADING, "trading"),
            (TransactionType.ITEM_MARKET, "itemMarket"),
            (TransactionType.WAGE, "wage"),
            (TransactionType.DONATION, "donation"),
            (TransactionType.ARTICLE_TIP, "articleTip"),
            (TransactionType.OPEN_CASE, "openCase"),
            (TransactionType.CRAFT_ITEM, "craftItem"),
            (TransactionType.DISMANTLE_ITEM, "dismantleItem"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestUpgradeType:
    def test_member_count(self):
        assert len(UpgradeType) == 8

    @pytest.mark.parametrize(
        "member, value",
        [
            (UpgradeType.BUNKER, "bunker"),
            (UpgradeType.BASE, "base"),
            (UpgradeType.PACIFICATION_CENTER, "pacificationCenter"),
            (UpgradeType.STORAGE, "storage"),
            (UpgradeType.AUTOMATED_ENGINE, "automatedEngine"),
            (UpgradeType.BREAK_ROOM, "breakRoom"),
            (UpgradeType.HEADQUARTERS, "headquarters"),
            (UpgradeType.DORMITORIES, "dormitories"),
        ],
    )
    def test_values(self, member, value):
        assert member == value


class TestEnumsAreStrings:
    """Every StrEnum member should be usable as a plain str."""

    @pytest.mark.parametrize(
        "enum_cls",
        [
            EventType,
            BattleDirection,
            BattleFilter,
            BattleRankingDataType,
            BattleRankingType,
            BattleRankingSide,
            RankingType,
            ArticleListType,
            TransactionType,
            UpgradeType,
        ],
    )
    def test_members_are_str_instances(self, enum_cls):
        for member in enum_cls:
            assert isinstance(member, str), f"{member!r} is not a str"

    @pytest.mark.parametrize(
        "enum_cls",
        [
            EventType,
            BattleDirection,
            BattleFilter,
            BattleRankingDataType,
            BattleRankingType,
            BattleRankingSide,
            RankingType,
            ArticleListType,
            TransactionType,
            UpgradeType,
        ],
    )
    def test_members_equal_their_value(self, enum_cls):
        for member in enum_cls:
            assert member == member.value
