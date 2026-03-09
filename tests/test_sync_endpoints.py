"""Tests for every synchronous WarEraClient endpoint method.

Each test mocks the HTTP layer with ``respx`` and verifies:
  1. The correct tRPC path is called.
  2. The JSON body sent matches what the API expects.
  3. The response JSON is returned unmodified.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from warera import WarEraClient
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

BASE_URL = "https://api2.warera.io/trpc"


# ── helpers ──────────────────────────────────────────────────────────────────


def _ok(payload: dict | list | None = None) -> httpx.Response:
    """Shortcut to build a 200 JSON response."""
    return httpx.Response(200, json=payload or {"result": {"data": "ok"}})


def _last_request(route: respx.Route) -> httpx.Request:
    """Return the last request captured by *route*."""
    assert route.called, "Route was never called"
    return route.calls.last.request


def _json_body(route: respx.Route) -> dict:
    """Return the parsed JSON body of the last request on *route*."""
    import json
    return json.loads(_last_request(route).content)


# ═════════════════════════════════════════════════════════════════════════════
#  Company
# ═════════════════════════════════════════════════════════════════════════════


class TestCompany:
    def test_get_company_by_id(self, mock_api, client):
        route = mock_api.post("/company.getById").mock(return_value=_ok({"id": "c1"}))
        result = client.get_company_by_id("c1")
        assert result == {"id": "c1"}
        assert _json_body(route) == {"companyId": "c1"}

    def test_get_companies_no_filters(self, mock_api, client):
        route = mock_api.post("/company.getCompanies").mock(return_value=_ok())
        client.get_companies()
        assert _json_body(route) == {}

    def test_get_companies_with_all_filters(self, mock_api, client):
        route = mock_api.post("/company.getCompanies").mock(return_value=_ok())
        client.get_companies(user_id="u1", per_page=25, cursor="abc")
        assert _json_body(route) == {"userId": "u1", "perPage": 25, "cursor": "abc"}

    def test_get_companies_partial_filters(self, mock_api, client):
        route = mock_api.post("/company.getCompanies").mock(return_value=_ok())
        client.get_companies(per_page=50)
        body = _json_body(route)
        assert body == {"perPage": 50}
        assert "userId" not in body
        assert "cursor" not in body


# ═════════════════════════════════════════════════════════════════════════════
#  Country
# ═════════════════════════════════════════════════════════════════════════════


class TestCountry:
    def test_get_country_by_id(self, mock_api, client):
        route = mock_api.post("/country.getCountryById").mock(
            return_value=_ok({"name": "Narnia"})
        )
        result = client.get_country_by_id("ct1")
        assert result == {"name": "Narnia"}
        assert _json_body(route) == {"countryId": "ct1"}

    def test_get_all_countries(self, mock_api, client):
        route = mock_api.post("/country.getAllCountries").mock(
            return_value=_ok([{"id": "ct1"}, {"id": "ct2"}])
        )
        result = client.get_all_countries()
        assert len(result) == 2
        assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  Event
# ═════════════════════════════════════════════════════════════════════════════


class TestEvent:
    def test_get_events_no_filters(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated()
        assert _json_body(route) == {}

    def test_get_events_with_limit_and_cursor(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated(limit=20, cursor="cur1")
        assert _json_body(route) == {"limit": 20, "cursor": "cur1"}

    def test_get_events_with_country_filter(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated(country_id="ct1")
        assert _json_body(route) == {"countryId": "ct1"}

    def test_get_events_with_event_types_strings(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated(event_types=["warDeclared", "battleOpened"])
        assert _json_body(route) == {"eventTypes": ["warDeclared", "battleOpened"]}

    def test_get_events_with_event_type_enums(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated(
            event_types=[EventType.WAR_DECLARED, EventType.PEACE_AGREEMENT]
        )
        body = _json_body(route)
        assert body["eventTypes"] == ["warDeclared", "peaceAgreement"]

    def test_get_events_all_params(self, mock_api, client):
        route = mock_api.post("/event.getEventsPaginated").mock(return_value=_ok())
        client.get_events_paginated(
            limit=5,
            cursor="pg2",
            country_id="ct3",
            event_types=[EventType.BANKRUPTCY],
        )
        assert _json_body(route) == {
            "limit": 5,
            "cursor": "pg2",
            "countryId": "ct3",
            "eventTypes": ["bankruptcy"],
        }


# ═════════════════════════════════════════════════════════════════════════════
#  Government
# ═════════════════════════════════════════════════════════════════════════════


class TestGovernment:
    def test_get_government_by_country_id(self, mock_api, client):
        route = mock_api.post("/government.getByCountryId").mock(return_value=_ok())
        client.get_government_by_country_id("ct1")
        assert _json_body(route) == {"countryId": "ct1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Region
# ═════════════════════════════════════════════════════════════════════════════


class TestRegion:
    def test_get_region_by_id(self, mock_api, client):
        route = mock_api.post("/region.getById").mock(return_value=_ok())
        client.get_region_by_id("r1")
        assert _json_body(route) == {"regionId": "r1"}

    def test_get_all_regions(self, mock_api, client):
        route = mock_api.post("/region.getRegionsObject").mock(return_value=_ok())
        client.get_all_regions()
        assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  Battle
# ═════════════════════════════════════════════════════════════════════════════


class TestBattle:
    def test_get_battle_by_id(self, mock_api, client):
        route = mock_api.post("/battle.getById").mock(return_value=_ok())
        client.get_battle_by_id("b1")
        assert _json_body(route) == {"battleId": "b1"}

    def test_get_live_battle_data_minimal(self, mock_api, client):
        route = mock_api.post("/battle.getLiveBattleData").mock(return_value=_ok())
        client.get_live_battle_data("b1")
        assert _json_body(route) == {"battleId": "b1"}

    def test_get_live_battle_data_with_round(self, mock_api, client):
        route = mock_api.post("/battle.getLiveBattleData").mock(return_value=_ok())
        client.get_live_battle_data("b1", round_number=3)
        assert _json_body(route) == {"battleId": "b1", "roundNumber": 3}

    def test_get_battles_no_filters(self, mock_api, client):
        route = mock_api.post("/battle.getBattles").mock(return_value=_ok())
        client.get_battles()
        assert _json_body(route) == {}

    def test_get_battles_active_only(self, mock_api, client):
        route = mock_api.post("/battle.getBattles").mock(return_value=_ok())
        client.get_battles(is_active=True, limit=5)
        body = _json_body(route)
        assert body["isActive"] is True
        assert body["limit"] == 5

    def test_get_battles_with_enum_filters(self, mock_api, client):
        route = mock_api.post("/battle.getBattles").mock(return_value=_ok())
        client.get_battles(
            direction=BattleDirection.FORWARD,
            filter=BattleFilter.YOUR_COUNTRY,
        )
        body = _json_body(route)
        assert body["direction"] == "forward"
        assert body["filter"] == "yourCountry"

    def test_get_battles_all_params(self, mock_api, client):
        route = mock_api.post("/battle.getBattles").mock(return_value=_ok())
        client.get_battles(
            is_active=False,
            limit=50,
            cursor="cur",
            direction="backward",
            filter="all",
            defender_region_id="r1",
            war_id="w1",
            country_id="ct1",
        )
        assert _json_body(route) == {
            "isActive": False,
            "limit": 50,
            "cursor": "cur",
            "direction": "backward",
            "filter": "all",
            "defenderRegionId": "r1",
            "warId": "w1",
            "countryId": "ct1",
        }


# ═════════════════════════════════════════════════════════════════════════════
#  Round
# ═════════════════════════════════════════════════════════════════════════════


class TestRound:
    def test_get_round_by_id(self, mock_api, client):
        route = mock_api.post("/round.getById").mock(return_value=_ok())
        client.get_round_by_id("rd1")
        assert _json_body(route) == {"roundId": "rd1"}

    def test_get_last_hits(self, mock_api, client):
        route = mock_api.post("/round.getLastHits").mock(return_value=_ok())
        client.get_last_hits("rd1")
        assert _json_body(route) == {"roundId": "rd1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Battle Ranking
# ═════════════════════════════════════════════════════════════════════════════


class TestBattleRanking:
    def test_required_params_only(self, mock_api, client):
        route = mock_api.post("/battleRanking.getRanking").mock(return_value=_ok())
        client.get_battle_ranking(
            data_type="damage", type="user", side="attacker"
        )
        assert _json_body(route) == {
            "dataType": "damage",
            "type": "user",
            "side": "attacker",
        }

    def test_with_enum_values(self, mock_api, client):
        route = mock_api.post("/battleRanking.getRanking").mock(return_value=_ok())
        client.get_battle_ranking(
            data_type=BattleRankingDataType.POINTS,
            type=BattleRankingType.COUNTRY,
            side=BattleRankingSide.DEFENDER,
        )
        assert _json_body(route) == {
            "dataType": "points",
            "type": "country",
            "side": "defender",
        }

    def test_with_optional_ids(self, mock_api, client):
        route = mock_api.post("/battleRanking.getRanking").mock(return_value=_ok())
        client.get_battle_ranking(
            data_type="money",
            type="mu",
            side="attacker",
            battle_id="b1",
            round_id="rd1",
            war_id="w1",
        )
        body = _json_body(route)
        assert body["battleId"] == "b1"
        assert body["roundId"] == "rd1"
        assert body["warId"] == "w1"

    def test_partial_optional_ids(self, mock_api, client):
        route = mock_api.post("/battleRanking.getRanking").mock(return_value=_ok())
        client.get_battle_ranking(
            data_type="damage", type="user", side="defender", battle_id="b1"
        )
        body = _json_body(route)
        assert body["battleId"] == "b1"
        assert "roundId" not in body
        assert "warId" not in body


# ═════════════════════════════════════════════════════════════════════════════
#  Item Trading
# ═════════════════════════════════════════════════════════════════════════════


class TestItemTrading:
    def test_get_item_prices(self, mock_api, client):
        route = mock_api.post("/itemTrading.getPrices").mock(
            return_value=_ok({"food": 1.5})
        )
        result = client.get_item_prices()
        assert result == {"food": 1.5}
        assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  Trading Order
# ═════════════════════════════════════════════════════════════════════════════


class TestTradingOrder:
    def test_get_top_orders_required_only(self, mock_api, client):
        route = mock_api.post("/tradingOrder.getTopOrders").mock(return_value=_ok())
        client.get_top_orders("food")
        assert _json_body(route) == {"itemCode": "food"}

    def test_get_top_orders_with_limit(self, mock_api, client):
        route = mock_api.post("/tradingOrder.getTopOrders").mock(return_value=_ok())
        client.get_top_orders("iron", limit=50)
        assert _json_body(route) == {"itemCode": "iron", "limit": 50}


# ═════════════════════════════════════════════════════════════════════════════
#  Item Offer
# ═════════════════════════════════════════════════════════════════════════════


class TestItemOffer:
    def test_get_item_offer_by_id(self, mock_api, client):
        route = mock_api.post("/itemOffer.getById").mock(return_value=_ok())
        client.get_item_offer_by_id("io1")
        assert _json_body(route) == {"itemOfferId": "io1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Work Offer
# ═════════════════════════════════════════════════════════════════════════════


class TestWorkOffer:
    def test_get_work_offer_by_id(self, mock_api, client):
        route = mock_api.post("/workOffer.getById").mock(return_value=_ok())
        client.get_work_offer_by_id("wo1")
        assert _json_body(route) == {"workOfferId": "wo1"}

    def test_get_work_offer_by_company_id(self, mock_api, client):
        route = mock_api.post("/workOffer.getWorkOfferByCompanyId").mock(
            return_value=_ok()
        )
        client.get_work_offer_by_company_id("c1")
        assert _json_body(route) == {"companyId": "c1"}

    def test_get_work_offers_paginated_no_filters(self, mock_api, client):
        route = mock_api.post("/workOffer.getWorkOffersPaginated").mock(
            return_value=_ok()
        )
        client.get_work_offers_paginated()
        assert _json_body(route) == {}

    def test_get_work_offers_paginated_all_filters(self, mock_api, client):
        route = mock_api.post("/workOffer.getWorkOffersPaginated").mock(
            return_value=_ok()
        )
        client.get_work_offers_paginated(
            user_id="u1",
            region_id="r1",
            cursor="abc",
            limit=20,
            energy=50.0,
            production=10.0,
            citizenship="ct1",
        )
        assert _json_body(route) == {
            "userId": "u1",
            "regionId": "r1",
            "cursor": "abc",
            "limit": 20,
            "energy": 50.0,
            "production": 10.0,
            "citizenship": "ct1",
        }


# ═════════════════════════════════════════════════════════════════════════════
#  Ranking
# ═════════════════════════════════════════════════════════════════════════════


class TestRanking:
    def test_get_ranking_with_string(self, mock_api, client):
        route = mock_api.post("/ranking.getRanking").mock(return_value=_ok())
        client.get_ranking("userLevel")
        assert _json_body(route) == {"rankingType": "userLevel"}

    def test_get_ranking_with_enum(self, mock_api, client):
        route = mock_api.post("/ranking.getRanking").mock(return_value=_ok())
        client.get_ranking(RankingType.COUNTRY_WEALTH)
        assert _json_body(route) == {"rankingType": "countryWealth"}


# ═════════════════════════════════════════════════════════════════════════════
#  Search
# ═════════════════════════════════════════════════════════════════════════════


class TestSearch:
    def test_search(self, mock_api, client):
        route = mock_api.post("/search.searchAnything").mock(return_value=_ok())
        client.search("hello world")
        assert _json_body(route) == {"searchText": "hello world"}


# ═════════════════════════════════════════════════════════════════════════════
#  Game Config
# ═════════════════════════════════════════════════════════════════════════════


class TestGameConfig:
    def test_get_game_dates(self, mock_api, client):
        route = mock_api.post("/gameConfig.getDates").mock(return_value=_ok())
        client.get_game_dates()
        assert _json_body(route) == {}

    def test_get_game_config(self, mock_api, client):
        route = mock_api.post("/gameConfig.getGameConfig").mock(return_value=_ok())
        client.get_game_config()
        assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  User
# ═════════════════════════════════════════════════════════════════════════════


class TestUser:
    def test_get_user_lite(self, mock_api, client):
        route = mock_api.post("/user.getUserLite").mock(
            return_value=_ok({"username": "alice"})
        )
        result = client.get_user_lite("u1")
        assert result == {"username": "alice"}
        assert _json_body(route) == {"userId": "u1"}

    def test_get_users_by_country_required_only(self, mock_api, client):
        route = mock_api.post("/user.getUsersByCountry").mock(return_value=_ok())
        client.get_users_by_country("ct1")
        assert _json_body(route) == {"countryId": "ct1"}

    def test_get_users_by_country_all_params(self, mock_api, client):
        route = mock_api.post("/user.getUsersByCountry").mock(return_value=_ok())
        client.get_users_by_country("ct1", limit=50, cursor="pg2")
        assert _json_body(route) == {"countryId": "ct1", "limit": 50, "cursor": "pg2"}

    def test_get_users_by_country_limit_only(self, mock_api, client):
        route = mock_api.post("/user.getUsersByCountry").mock(return_value=_ok())
        client.get_users_by_country("ct1", limit=10)
        body = _json_body(route)
        assert body == {"countryId": "ct1", "limit": 10}
        assert "cursor" not in body


# ═════════════════════════════════════════════════════════════════════════════
#  Article
# ═════════════════════════════════════════════════════════════════════════════


class TestArticle:
    def test_get_article_by_id(self, mock_api, client):
        route = mock_api.post("/article.getArticleById").mock(return_value=_ok())
        client.get_article_by_id("a1")
        assert _json_body(route) == {"articleId": "a1"}

    def test_get_article_lite_by_id(self, mock_api, client):
        route = mock_api.post("/article.getArticleLiteById").mock(return_value=_ok())
        client.get_article_lite_by_id("a1")
        assert _json_body(route) == {"articleId": "a1"}

    def test_get_articles_paginated_required_only(self, mock_api, client):
        route = mock_api.post("/article.getArticlesPaginated").mock(return_value=_ok())
        client.get_articles_paginated("daily")
        assert _json_body(route) == {"type": "daily"}

    def test_get_articles_paginated_with_enum(self, mock_api, client):
        route = mock_api.post("/article.getArticlesPaginated").mock(return_value=_ok())
        client.get_articles_paginated(ArticleListType.TOP)
        assert _json_body(route) == {"type": "top"}

    def test_get_articles_paginated_all_params(self, mock_api, client):
        route = mock_api.post("/article.getArticlesPaginated").mock(return_value=_ok())
        client.get_articles_paginated(
            "weekly",
            limit=20,
            cursor="c1",
            user_id="u1",
            categories=["news", "politics"],
            languages=["en", "fr"],
            positive_score_only=True,
        )
        assert _json_body(route) == {
            "type": "weekly",
            "limit": 20,
            "cursor": "c1",
            "userId": "u1",
            "categories": ["news", "politics"],
            "languages": ["en", "fr"],
            "positiveScoreOnly": True,
        }

    def test_get_articles_paginated_categories_only(self, mock_api, client):
        route = mock_api.post("/article.getArticlesPaginated").mock(return_value=_ok())
        client.get_articles_paginated("last", categories=["sports"])
        body = _json_body(route)
        assert body["type"] == "last"
        assert body["categories"] == ["sports"]
        assert "languages" not in body


# ═════════════════════════════════════════════════════════════════════════════
#  Military Unit (MU)
# ═════════════════════════════════════════════════════════════════════════════


class TestMilitaryUnit:
    def test_get_mu_by_id(self, mock_api, client):
        route = mock_api.post("/mu.getById").mock(return_value=_ok())
        client.get_mu_by_id("mu1")
        assert _json_body(route) == {"muId": "mu1"}

    def test_get_mus_paginated_no_filters(self, mock_api, client):
        route = mock_api.post("/mu.getManyPaginated").mock(return_value=_ok())
        client.get_mus_paginated()
        assert _json_body(route) == {}

    def test_get_mus_paginated_all_filters(self, mock_api, client):
        route = mock_api.post("/mu.getManyPaginated").mock(return_value=_ok())
        client.get_mus_paginated(
            limit=10, cursor="c1", member_id="m1", user_id="u1", search="legion"
        )
        assert _json_body(route) == {
            "limit": 10,
            "cursor": "c1",
            "memberId": "m1",
            "userId": "u1",
            "search": "legion",
        }


# ═════════════════════════════════════════════════════════════════════════════
#  Transaction
# ═════════════════════════════════════════════════════════════════════════════


class TestTransaction:
    def test_get_transactions_no_filters(self, mock_api, client):
        route = mock_api.post("/transaction.getPaginatedTransactions").mock(
            return_value=_ok()
        )
        client.get_transactions_paginated()
        assert _json_body(route) == {}

    def test_get_transactions_single_type_string(self, mock_api, client):
        route = mock_api.post("/transaction.getPaginatedTransactions").mock(
            return_value=_ok()
        )
        client.get_transactions_paginated(transaction_type="wage")
        assert _json_body(route) == {"transactionType": "wage"}

    def test_get_transactions_single_type_enum(self, mock_api, client):
        route = mock_api.post("/transaction.getPaginatedTransactions").mock(
            return_value=_ok()
        )
        client.get_transactions_paginated(
            transaction_type=TransactionType.DONATION
        )
        assert _json_body(route) == {"transactionType": "donation"}

    def test_get_transactions_multiple_types(self, mock_api, client):
        route = mock_api.post("/transaction.getPaginatedTransactions").mock(
            return_value=_ok()
        )
        client.get_transactions_paginated(
            transaction_type=[TransactionType.TRADING, TransactionType.WAGE]
        )
        assert _json_body(route) == {
            "transactionType": ["trading", "wage"]
        }

    def test_get_transactions_all_params(self, mock_api, client):
        route = mock_api.post("/transaction.getPaginatedTransactions").mock(
            return_value=_ok()
        )
        client.get_transactions_paginated(
            limit=25,
            cursor="c",
            user_id="u1",
            mu_id="mu1",
            country_id="ct1",
            party_id="p1",
            item_code="food",
            transaction_type="itemMarket",
        )
        assert _json_body(route) == {
            "limit": 25,
            "cursor": "c",
            "userId": "u1",
            "muId": "mu1",
            "countryId": "ct1",
            "partyId": "p1",
            "itemCode": "food",
            "transactionType": "itemMarket",
        }


# ═════════════════════════════════════════════════════════════════════════════
#  Upgrade
# ═════════════════════════════════════════════════════════════════════════════


class TestUpgrade:
    def test_get_upgrade_required_only(self, mock_api, client):
        route = mock_api.post("/upgrade.getUpgradeByTypeAndEntity").mock(
            return_value=_ok()
        )
        client.get_upgrade("bunker")
        assert _json_body(route) == {"upgradeType": "bunker"}

    def test_get_upgrade_with_enum(self, mock_api, client):
        route = mock_api.post("/upgrade.getUpgradeByTypeAndEntity").mock(
            return_value=_ok()
        )
        client.get_upgrade(UpgradeType.STORAGE, company_id="c1")
        assert _json_body(route) == {"upgradeType": "storage", "companyId": "c1"}

    def test_get_upgrade_with_all_entities(self, mock_api, client):
        route = mock_api.post("/upgrade.getUpgradeByTypeAndEntity").mock(
            return_value=_ok()
        )
        client.get_upgrade(
            UpgradeType.HEADQUARTERS, region_id="r1", company_id="c1", mu_id="mu1"
        )
        assert _json_body(route) == {
            "upgradeType": "headquarters",
            "regionId": "r1",
            "companyId": "c1",
            "muId": "mu1",
        }

    def test_get_upgrade_region_only(self, mock_api, client):
        route = mock_api.post("/upgrade.getUpgradeByTypeAndEntity").mock(
            return_value=_ok()
        )
        client.get_upgrade("base", region_id="r1")
        body = _json_body(route)
        assert body == {"upgradeType": "base", "regionId": "r1"}
        assert "companyId" not in body
        assert "muId" not in body


# ═════════════════════════════════════════════════════════════════════════════
#  Worker
# ═════════════════════════════════════════════════════════════════════════════


class TestWorker:
    def test_get_workers_no_filters(self, mock_api, client):
        route = mock_api.post("/worker.getWorkers").mock(return_value=_ok())
        client.get_workers()
        assert _json_body(route) == {}

    def test_get_workers_by_company(self, mock_api, client):
        route = mock_api.post("/worker.getWorkers").mock(return_value=_ok())
        client.get_workers(company_id="c1")
        assert _json_body(route) == {"companyId": "c1"}

    def test_get_workers_by_user(self, mock_api, client):
        route = mock_api.post("/worker.getWorkers").mock(return_value=_ok())
        client.get_workers(user_id="u1")
        assert _json_body(route) == {"userId": "u1"}

    def test_get_workers_both_filters(self, mock_api, client):
        route = mock_api.post("/worker.getWorkers").mock(return_value=_ok())
        client.get_workers(company_id="c1", user_id="u1")
        assert _json_body(route) == {"companyId": "c1", "userId": "u1"}

    def test_get_total_workers_count(self, mock_api, client):
        route = mock_api.post("/worker.getTotalWorkersCount").mock(
            return_value=_ok({"count": 42})
        )
        result = client.get_total_workers_count("u1")
        assert result == {"count": 42}
        assert _json_body(route) == {"userId": "u1"}
