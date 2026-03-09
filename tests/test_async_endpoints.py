"""Tests for every asynchronous AsyncWarEraClient endpoint method.

Mirrors the sync test suite but exercises the ``async/await`` code paths.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from warera import AsyncWarEraClient
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
from warera.exceptions import WarEraAPIError, WarEraConnectionError

BASE_URL = "https://api2.warera.io/trpc"


# ── helpers ──────────────────────────────────────────────────────────────────


def _ok(payload: dict | list | None = None) -> httpx.Response:
    return httpx.Response(200, json=payload or {"result": {"data": "ok"}})


def _json_body(route: respx.Route) -> dict:
    import json
    return json.loads(route.calls.last.request.content)


# ═════════════════════════════════════════════════════════════════════════════
#  Company
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncCompany:
    @pytest.mark.asyncio
    async def test_get_company_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/company.getById").mock(
                    return_value=_ok({"id": "c1"})
                )
                result = await client.get_company_by_id("c1")
                assert result == {"id": "c1"}
                assert _json_body(route) == {"companyId": "c1"}

    @pytest.mark.asyncio
    async def test_get_companies_no_filters(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/company.getCompanies").mock(return_value=_ok())
                await client.get_companies()
                assert _json_body(route) == {}

    @pytest.mark.asyncio
    async def test_get_companies_all_filters(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/company.getCompanies").mock(return_value=_ok())
                await client.get_companies(user_id="u1", per_page=25, cursor="abc")
                assert _json_body(route) == {
                    "userId": "u1",
                    "perPage": 25,
                    "cursor": "abc",
                }


# ═════════════════════════════════════════════════════════════════════════════
#  Country
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncCountry:
    @pytest.mark.asyncio
    async def test_get_country_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/country.getCountryById").mock(return_value=_ok())
                await client.get_country_by_id("ct1")
                assert _json_body(route) == {"countryId": "ct1"}

    @pytest.mark.asyncio
    async def test_get_all_countries(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/country.getAllCountries").mock(
                    return_value=_ok([{"id": "ct1"}])
                )
                result = await client.get_all_countries()
                assert result == [{"id": "ct1"}]
                assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  Event
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncEvent:
    @pytest.mark.asyncio
    async def test_get_events_no_filters(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/event.getEventsPaginated").mock(return_value=_ok())
                await client.get_events_paginated()
                assert _json_body(route) == {}

    @pytest.mark.asyncio
    async def test_get_events_with_enum_types(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/event.getEventsPaginated").mock(return_value=_ok())
                await client.get_events_paginated(
                    event_types=[EventType.WAR_DECLARED, EventType.BATTLE_ENDED],
                    limit=5,
                )
                body = _json_body(route)
                assert body["eventTypes"] == ["warDeclared", "battleEnded"]
                assert body["limit"] == 5


# ═════════════════════════════════════════════════════════════════════════════
#  Government
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncGovernment:
    @pytest.mark.asyncio
    async def test_get_government_by_country_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/government.getByCountryId").mock(
                    return_value=_ok()
                )
                await client.get_government_by_country_id("ct1")
                assert _json_body(route) == {"countryId": "ct1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Region
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncRegion:
    @pytest.mark.asyncio
    async def test_get_region_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/region.getById").mock(return_value=_ok())
                await client.get_region_by_id("r1")
                assert _json_body(route) == {"regionId": "r1"}

    @pytest.mark.asyncio
    async def test_get_all_regions(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/region.getRegionsObject").mock(return_value=_ok())
                await client.get_all_regions()
                assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  Battle
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncBattle:
    @pytest.mark.asyncio
    async def test_get_battle_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/battle.getById").mock(return_value=_ok())
                await client.get_battle_by_id("b1")
                assert _json_body(route) == {"battleId": "b1"}

    @pytest.mark.asyncio
    async def test_get_live_battle_data(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/battle.getLiveBattleData").mock(return_value=_ok())
                await client.get_live_battle_data("b1", round_number=2)
                assert _json_body(route) == {"battleId": "b1", "roundNumber": 2}

    @pytest.mark.asyncio
    async def test_get_battles_with_enums(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/battle.getBattles").mock(return_value=_ok())
                await client.get_battles(
                    direction=BattleDirection.BACKWARD,
                    filter=BattleFilter.ALL,
                    is_active=True,
                )
                body = _json_body(route)
                assert body["direction"] == "backward"
                assert body["filter"] == "all"
                assert body["isActive"] is True


# ═════════════════════════════════════════════════════════════════════════════
#  Round
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncRound:
    @pytest.mark.asyncio
    async def test_get_round_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/round.getById").mock(return_value=_ok())
                await client.get_round_by_id("rd1")
                assert _json_body(route) == {"roundId": "rd1"}

    @pytest.mark.asyncio
    async def test_get_last_hits(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/round.getLastHits").mock(return_value=_ok())
                await client.get_last_hits("rd1")
                assert _json_body(route) == {"roundId": "rd1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Battle Ranking
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncBattleRanking:
    @pytest.mark.asyncio
    async def test_with_enums(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/battleRanking.getRanking").mock(return_value=_ok())
                await client.get_battle_ranking(
                    data_type=BattleRankingDataType.MONEY,
                    type=BattleRankingType.MU,
                    side=BattleRankingSide.ATTACKER,
                    war_id="w1",
                )
                body = _json_body(route)
                assert body == {
                    "dataType": "money",
                    "type": "mu",
                    "side": "attacker",
                    "warId": "w1",
                }


# ═════════════════════════════════════════════════════════════════════════════
#  Item Trading
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncItemTrading:
    @pytest.mark.asyncio
    async def test_get_item_prices(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/itemTrading.getPrices").mock(
                    return_value=_ok({"food": 2.0})
                )
                result = await client.get_item_prices()
                assert result == {"food": 2.0}


# ═════════════════════════════════════════════════════════════════════════════
#  Trading Order
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncTradingOrder:
    @pytest.mark.asyncio
    async def test_get_top_orders(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/tradingOrder.getTopOrders").mock(return_value=_ok())
                await client.get_top_orders("iron", limit=20)
                assert _json_body(route) == {"itemCode": "iron", "limit": 20}


# ═════════════════════════════════════════════════════════════════════════════
#  Item Offer
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncItemOffer:
    @pytest.mark.asyncio
    async def test_get_item_offer_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/itemOffer.getById").mock(return_value=_ok())
                await client.get_item_offer_by_id("io1")
                assert _json_body(route) == {"itemOfferId": "io1"}


# ═════════════════════════════════════════════════════════════════════════════
#  Work Offer
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncWorkOffer:
    @pytest.mark.asyncio
    async def test_get_work_offer_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/workOffer.getById").mock(return_value=_ok())
                await client.get_work_offer_by_id("wo1")
                assert _json_body(route) == {"workOfferId": "wo1"}

    @pytest.mark.asyncio
    async def test_get_work_offer_by_company_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/workOffer.getWorkOfferByCompanyId").mock(
                    return_value=_ok()
                )
                await client.get_work_offer_by_company_id("c1")
                assert _json_body(route) == {"companyId": "c1"}

    @pytest.mark.asyncio
    async def test_get_work_offers_paginated_all(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/workOffer.getWorkOffersPaginated").mock(
                    return_value=_ok()
                )
                await client.get_work_offers_paginated(
                    user_id="u1",
                    region_id="r1",
                    limit=15,
                    energy=30.0,
                    production=5.0,
                    citizenship="ct1",
                )
                body = _json_body(route)
                assert body["userId"] == "u1"
                assert body["regionId"] == "r1"
                assert body["limit"] == 15
                assert body["energy"] == 30.0
                assert body["production"] == 5.0
                assert body["citizenship"] == "ct1"


# ═════════════════════════════════════════════════════════════════════════════
#  Ranking
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncRanking:
    @pytest.mark.asyncio
    async def test_get_ranking(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/ranking.getRanking").mock(return_value=_ok())
                await client.get_ranking(RankingType.MU_BOUNTY)
                assert _json_body(route) == {"rankingType": "muBounty"}


# ═════════════════════════════════════════════════════════════════════════════
#  Search
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncSearch:
    @pytest.mark.asyncio
    async def test_search(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/search.searchAnything").mock(return_value=_ok())
                await client.search("test query")
                assert _json_body(route) == {"searchText": "test query"}


# ═════════════════════════════════════════════════════════════════════════════
#  Game Config
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncGameConfig:
    @pytest.mark.asyncio
    async def test_get_game_dates(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/gameConfig.getDates").mock(return_value=_ok())
                await client.get_game_dates()
                assert _json_body(route) == {}

    @pytest.mark.asyncio
    async def test_get_game_config(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/gameConfig.getGameConfig").mock(return_value=_ok())
                await client.get_game_config()
                assert _json_body(route) == {}


# ═════════════════════════════════════════════════════════════════════════════
#  User
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncUser:
    @pytest.mark.asyncio
    async def test_get_user_lite(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/user.getUserLite").mock(
                    return_value=_ok({"username": "bob"})
                )
                result = await client.get_user_lite("u1")
                assert result == {"username": "bob"}

    @pytest.mark.asyncio
    async def test_get_users_by_country(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/user.getUsersByCountry").mock(return_value=_ok())
                await client.get_users_by_country("ct1", limit=20, cursor="c")
                assert _json_body(route) == {
                    "countryId": "ct1",
                    "limit": 20,
                    "cursor": "c",
                }


# ═════════════════════════════════════════════════════════════════════════════
#  Article
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncArticle:
    @pytest.mark.asyncio
    async def test_get_article_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/article.getArticleById").mock(return_value=_ok())
                await client.get_article_by_id("a1")
                assert _json_body(route) == {"articleId": "a1"}

    @pytest.mark.asyncio
    async def test_get_article_lite_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/article.getArticleLiteById").mock(
                    return_value=_ok()
                )
                await client.get_article_lite_by_id("a1")
                assert _json_body(route) == {"articleId": "a1"}

    @pytest.mark.asyncio
    async def test_get_articles_paginated_all(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/article.getArticlesPaginated").mock(
                    return_value=_ok()
                )
                await client.get_articles_paginated(
                    ArticleListType.SUBSCRIPTIONS,
                    limit=10,
                    languages=["de"],
                    positive_score_only=False,
                )
                body = _json_body(route)
                assert body["type"] == "subscriptions"
                assert body["limit"] == 10
                assert body["languages"] == ["de"]
                assert body["positiveScoreOnly"] is False


# ═════════════════════════════════════════════════════════════════════════════
#  Military Unit
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncMU:
    @pytest.mark.asyncio
    async def test_get_mu_by_id(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/mu.getById").mock(return_value=_ok())
                await client.get_mu_by_id("mu1")
                assert _json_body(route) == {"muId": "mu1"}

    @pytest.mark.asyncio
    async def test_get_mus_paginated(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/mu.getManyPaginated").mock(return_value=_ok())
                await client.get_mus_paginated(search="alpha", limit=5)
                assert _json_body(route) == {"search": "alpha", "limit": 5}


# ═════════════════════════════════════════════════════════════════════════════
#  Transaction
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncTransaction:
    @pytest.mark.asyncio
    async def test_get_transactions_multiple_types(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/transaction.getPaginatedTransactions").mock(
                    return_value=_ok()
                )
                await client.get_transactions_paginated(
                    transaction_type=[
                        TransactionType.OPEN_CASE,
                        TransactionType.CRAFT_ITEM,
                    ]
                )
                assert _json_body(route) == {
                    "transactionType": ["openCase", "craftItem"]
                }

    @pytest.mark.asyncio
    async def test_get_transactions_single_string(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/transaction.getPaginatedTransactions").mock(
                    return_value=_ok()
                )
                await client.get_transactions_paginated(transaction_type="wage")
                assert _json_body(route) == {"transactionType": "wage"}


# ═════════════════════════════════════════════════════════════════════════════
#  Upgrade
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncUpgrade:
    @pytest.mark.asyncio
    async def test_get_upgrade(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/upgrade.getUpgradeByTypeAndEntity").mock(
                    return_value=_ok()
                )
                await client.get_upgrade(UpgradeType.DORMITORIES, mu_id="mu1")
                assert _json_body(route) == {
                    "upgradeType": "dormitories",
                    "muId": "mu1",
                }


# ═════════════════════════════════════════════════════════════════════════════
#  Worker
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncWorker:
    @pytest.mark.asyncio
    async def test_get_workers(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/worker.getWorkers").mock(return_value=_ok())
                await client.get_workers(company_id="c1", user_id="u1")
                assert _json_body(route) == {"companyId": "c1", "userId": "u1"}

    @pytest.mark.asyncio
    async def test_get_total_workers_count(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                route = mock.post("/worker.getTotalWorkersCount").mock(
                    return_value=_ok({"count": 10})
                )
                result = await client.get_total_workers_count("u1")
                assert result == {"count": 10}


# ═════════════════════════════════════════════════════════════════════════════
#  Error handling (async)
# ═════════════════════════════════════════════════════════════════════════════


class TestAsyncErrors:
    @pytest.mark.asyncio
    async def test_api_error_raised(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                mock.post("/user.getUserLite").mock(
                    return_value=httpx.Response(404, text="not found")
                )
                with pytest.raises(WarEraAPIError) as exc_info:
                    await client.get_user_lite("bad")
                assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_connection_error_raised(self):
        async with AsyncWarEraClient() as client:
            with respx.mock(base_url=BASE_URL) as mock:
                mock.post("/country.getAllCountries").mock(
                    side_effect=httpx.ConnectError("refused")
                )
                with pytest.raises(WarEraConnectionError):
                    await client.get_all_countries()
