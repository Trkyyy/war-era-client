"""Synchronous and asynchronous clients for the WarEra API.

Usage::

    from warera import WarEraClient

    client = WarEraClient(api_key="your-api-key")
    user = client.get_user_lite(user_id="abc123")
    print(user)

Or with ``async``::

    from warera import AsyncWarEraClient

    async with AsyncWarEraClient(api_key="your-api-key") as client:
        user = await client.get_user_lite(user_id="abc123")
"""

from __future__ import annotations

from typing import Any, Sequence

import httpx

from warera.exceptions import WarEraAPIError, WarEraConnectionError

_DEFAULT_BASE_URL = "https://api2.warera.io/trpc"


# ─── helpers ─────────────────────────────────────────────────────────────────


def _strip_nones(data: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of *data* with all ``None``-valued keys removed."""
    return {k: v for k, v in data.items() if v is not None}


def _handle_response(response: httpx.Response) -> Any:
    """Raise on HTTP errors and return the parsed JSON body."""
    if response.status_code != 200:
        try:
            detail = response.text
        except Exception:
            detail = None
        raise WarEraAPIError(response.status_code, detail)
    return response.json()


# ═══════════════════════════════════════════════════════════════════════════════
#  Synchronous client
# ═══════════════════════════════════════════════════════════════════════════════


class WarEraClient:
    """Synchronous Python client for the WarEra API.

    Parameters
    ----------
    api_key:
        API key for authentication. Sent as ``X-API-Key`` header.
    base_url:
        Override the default API base URL.
    timeout:
        Request timeout in seconds (default 30).
    **client_kwargs:
        Extra keyword arguments forwarded to :class:`httpx.Client`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        **client_kwargs: Any,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        self._client = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            headers=headers,
            **client_kwargs,
        )

    # -- lifecycle -------------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP transport."""
        self._client.close()

    def __enter__(self) -> WarEraClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    # -- internal --------------------------------------------------------------

    def _post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        try:
            resp = self._client.post(f"/{path}", json=body or {})
        except httpx.ConnectError as exc:
            raise WarEraConnectionError(str(exc)) from exc
        return _handle_response(resp)

    # ── Company ──────────────────────────────────────────────────────────────

    def get_company_by_id(self, company_id: str) -> Any:
        """Retrieve detailed information about a specific company.

        Parameters
        ----------
        company_id:
            The unique identifier of the company.
        """
        return self._post("company.getById", {"companyId": company_id})

    def get_companies(
        self,
        *,
        user_id: str | None = None,
        per_page: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of companies.

        Parameters
        ----------
        user_id:
            Filter companies by owner user ID.
        per_page:
            Number of companies per page (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        """
        return self._post(
            "company.getCompanies",
            _strip_nones({"userId": user_id, "perPage": per_page, "cursor": cursor}),
        )

    # ── Country ──────────────────────────────────────────────────────────────

    def get_country_by_id(self, country_id: str) -> Any:
        """Retrieve detailed information about a specific country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        """
        return self._post("country.getCountryById", {"countryId": country_id})

    def get_all_countries(self) -> Any:
        """Retrieve a list of all available countries."""
        return self._post("country.getAllCountries")

    # ── Event ────────────────────────────────────────────────────────────────

    def get_events_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        country_id: str | None = None,
        event_types: Sequence[str] | None = None,
    ) -> Any:
        """Retrieve a paginated list of events.

        Parameters
        ----------
        limit:
            Maximum number of events to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        country_id:
            Filter events by country ID.
        event_types:
            Filter events by event types (use :class:`~warera.enums.EventType`).
        """
        body: dict[str, Any] = _strip_nones({
            "limit": limit,
            "cursor": cursor,
            "countryId": country_id,
        })
        if event_types is not None:
            body["eventTypes"] = list(event_types)
        return self._post("event.getEventsPaginated", body)

    # ── Government ───────────────────────────────────────────────────────────

    def get_government_by_country_id(self, country_id: str) -> Any:
        """Retrieve government information for a specific country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        """
        return self._post("government.getByCountryId", {"countryId": country_id})

    # ── Region ───────────────────────────────────────────────────────────────

    def get_region_by_id(self, region_id: str) -> Any:
        """Retrieve detailed information about a specific region.

        Parameters
        ----------
        region_id:
            The unique identifier of the region.
        """
        return self._post("region.getById", {"regionId": region_id})

    def get_all_regions(self) -> Any:
        """Retrieve a complete object containing all available regions."""
        return self._post("region.getRegionsObject")

    # ── Battle ───────────────────────────────────────────────────────────────

    def get_battle_by_id(self, battle_id: str) -> Any:
        """Retrieve detailed information about a specific battle.

        Parameters
        ----------
        battle_id:
            The unique identifier of the battle.
        """
        return self._post("battle.getById", {"battleId": battle_id})

    def get_live_battle_data(
        self,
        battle_id: str,
        *,
        round_number: int | None = None,
    ) -> Any:
        """Retrieve real-time battle data including current round information.

        Parameters
        ----------
        battle_id:
            The unique identifier of the battle.
        round_number:
            Optional specific round number to retrieve.
        """
        body: dict[str, Any] = {"battleId": battle_id}
        if round_number is not None:
            body["roundNumber"] = round_number
        return self._post("battle.getLiveBattleData", body)

    def get_battles(
        self,
        *,
        is_active: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        direction: str | None = None,
        filter: str | None = None,
        defender_region_id: str | None = None,
        war_id: str | None = None,
        country_id: str | None = None,
    ) -> Any:
        """Retrieve a list of battles.

        Parameters
        ----------
        is_active:
            Whether to get active battles.
        limit:
            Maximum number of battles to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        direction:
            ``"forward"`` or ``"backward"`` (see :class:`~warera.enums.BattleDirection`).
        filter:
            ``"all"``, ``"yourCountry"``, or ``"yourEnemies"``
            (see :class:`~warera.enums.BattleFilter`).
        defender_region_id:
            Filter battles by defender region ID.
        war_id:
            Filter battles by war ID.
        country_id:
            Filter battles by country ID.
        """
        return self._post(
            "battle.getBattles",
            _strip_nones({
                "isActive": is_active,
                "limit": limit,
                "cursor": cursor,
                "direction": direction,
                "filter": filter,
                "defenderRegionId": defender_region_id,
                "warId": war_id,
                "countryId": country_id,
            }),
        )

    # ── Round ────────────────────────────────────────────────────────────────

    def get_round_by_id(self, round_id: str) -> Any:
        """Retrieve detailed information about a specific battle round.

        Parameters
        ----------
        round_id:
            The unique identifier of the round.
        """
        return self._post("round.getById", {"roundId": round_id})

    def get_last_hits(self, round_id: str) -> Any:
        """Retrieve the most recent hits/damages in a specific battle round.

        Parameters
        ----------
        round_id:
            The unique identifier of the round.
        """
        return self._post("round.getLastHits", {"roundId": round_id})

    # ── Battle Ranking ───────────────────────────────────────────────────────

    def get_battle_ranking(
        self,
        *,
        data_type: str,
        type: str,
        side: str,
        battle_id: str | None = None,
        round_id: str | None = None,
        war_id: str | None = None,
    ) -> Any:
        """Retrieve battle rankings.

        Parameters
        ----------
        data_type:
            Type of ranking data: ``"damage"``, ``"points"``, or ``"money"``
            (see :class:`~warera.enums.BattleRankingDataType`).
        type:
            Rank by ``"user"``, ``"country"``, or ``"mu"``
            (see :class:`~warera.enums.BattleRankingType`).
        side:
            ``"attacker"`` or ``"defender"``
            (see :class:`~warera.enums.BattleRankingSide`).
        battle_id:
            Optional battle ID to filter rankings.
        round_id:
            Optional round ID to filter rankings.
        war_id:
            Optional war ID to filter rankings.
        """
        body: dict[str, Any] = {
            "dataType": data_type,
            "type": type,
            "side": side,
        }
        if battle_id is not None:
            body["battleId"] = battle_id
        if round_id is not None:
            body["roundId"] = round_id
        if war_id is not None:
            body["warId"] = war_id
        return self._post("battleRanking.getRanking", body)

    # ── Item Trading ─────────────────────────────────────────────────────────

    def get_item_prices(self) -> Any:
        """Retrieve current market prices for all tradeable items."""
        return self._post("itemTrading.getPrices")

    # ── Trading Order ────────────────────────────────────────────────────────

    def get_top_orders(
        self,
        item_code: str,
        *,
        limit: int | None = None,
    ) -> Any:
        """Retrieve the best orders for an item.

        Parameters
        ----------
        item_code:
            The item code to get orders for.
        limit:
            Maximum number of orders to return (1-100, default 10).
        """
        body: dict[str, Any] = {"itemCode": item_code}
        if limit is not None:
            body["limit"] = limit
        return self._post("tradingOrder.getTopOrders", body)

    # ── Item Offer ───────────────────────────────────────────────────────────

    def get_item_offer_by_id(self, item_offer_id: str) -> Any:
        """Retrieve detailed information about a specific item offer.

        Parameters
        ----------
        item_offer_id:
            The unique identifier of the item offer.
        """
        return self._post("itemOffer.getById", {"itemOfferId": item_offer_id})

    # ── Work Offer ───────────────────────────────────────────────────────────

    def get_work_offer_by_id(self, work_offer_id: str) -> Any:
        """Retrieve detailed information about a specific work offer.

        Parameters
        ----------
        work_offer_id:
            The unique identifier of the work offer.
        """
        return self._post("workOffer.getById", {"workOfferId": work_offer_id})

    def get_work_offer_by_company_id(self, company_id: str) -> Any:
        """Retrieve the work offer for a specific company.

        Parameters
        ----------
        company_id:
            The unique identifier of the company.
        """
        return self._post("workOffer.getWorkOfferByCompanyId", {"companyId": company_id})

    def get_work_offers_paginated(
        self,
        *,
        user_id: str | None = None,
        region_id: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        energy: float | None = None,
        production: float | None = None,
        citizenship: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of work offers.

        Parameters
        ----------
        user_id:
            Filter by user ID.
        region_id:
            Filter by region ID.
        cursor:
            Pagination cursor for the next page.
        limit:
            Number of work offers per page (default 10).
        energy:
            Minimum energy filter (>= 0).
        production:
            Minimum production filter (>= 0).
        citizenship:
            Filter by citizenship country.
        """
        return self._post(
            "workOffer.getWorkOffersPaginated",
            _strip_nones({
                "userId": user_id,
                "regionId": region_id,
                "cursor": cursor,
                "limit": limit,
                "energy": energy,
                "production": production,
                "citizenship": citizenship,
            }),
        )

    # ── Ranking ──────────────────────────────────────────────────────────────

    def get_ranking(self, ranking_type: str) -> Any:
        """Retrieve ranking data for the specified ranking type.

        Parameters
        ----------
        ranking_type:
            The type of ranking to retrieve
            (see :class:`~warera.enums.RankingType`).
        """
        return self._post("ranking.getRanking", {"rankingType": ranking_type})

    # ── Search ───────────────────────────────────────────────────────────────

    def search(self, search_text: str) -> Any:
        """Perform a global search across all entities.

        Parameters
        ----------
        search_text:
            The search query string.
        """
        return self._post("search.searchAnything", {"searchText": search_text})

    # ── Game Config ──────────────────────────────────────────────────────────

    def get_game_dates(self) -> Any:
        """Retrieve game-related dates and timings."""
        return self._post("gameConfig.getDates")

    def get_game_config(self) -> Any:
        """Retrieve the static game configuration."""
        return self._post("gameConfig.getGameConfig")

    # ── User ─────────────────────────────────────────────────────────────────

    def get_user_lite(self, user_id: str) -> Any:
        """Retrieve basic public information about a user.

        Parameters
        ----------
        user_id:
            The unique identifier of the user.
        """
        return self._post("user.getUserLite", {"userId": user_id})

    def get_users_by_country(
        self,
        country_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        """Retrieve a list of users by country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        limit:
            Maximum number of users to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        """
        body: dict[str, Any] = {"countryId": country_id}
        if limit is not None:
            body["limit"] = limit
        if cursor is not None:
            body["cursor"] = cursor
        return self._post("user.getUsersByCountry", body)

    # ── Article ──────────────────────────────────────────────────────────────

    def get_article_by_id(self, article_id: str) -> Any:
        """Retrieve detailed information about a specific article.

        Parameters
        ----------
        article_id:
            The ID of the article to get.
        """
        return self._post("article.getArticleById", {"articleId": article_id})

    def get_article_lite_by_id(self, article_id: str) -> Any:
        """Retrieve only the title and basic stats of an article (no view counted).

        Parameters
        ----------
        article_id:
            The ID of the article to get.
        """
        return self._post("article.getArticleLiteById", {"articleId": article_id})

    def get_articles_paginated(
        self,
        type: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        user_id: str | None = None,
        categories: Sequence[str] | None = None,
        languages: Sequence[str] | None = None,
        positive_score_only: bool | None = None,
    ) -> Any:
        """Retrieve a paginated list of articles.

        Parameters
        ----------
        type:
            The type of articles to get: ``"daily"``, ``"weekly"``, ``"top"``,
            ``"my"``, ``"subscriptions"``, or ``"last"``
            (see :class:`~warera.enums.ArticleListType`).
        limit:
            Maximum number of articles to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        user_id:
            The user ID to get articles for.
        categories:
            Filter by article categories.
        languages:
            Filter by article languages.
        positive_score_only:
            Only show articles with a positive score.
        """
        body: dict[str, Any] = {"type": type}
        body.update(_strip_nones({
            "limit": limit,
            "cursor": cursor,
            "userId": user_id,
            "positiveScoreOnly": positive_score_only,
        }))
        if categories is not None:
            body["categories"] = list(categories)
        if languages is not None:
            body["languages"] = list(languages)
        return self._post("article.getArticlesPaginated", body)

    # ── Military Unit (MU) ───────────────────────────────────────────────────

    def get_mu_by_id(self, mu_id: str) -> Any:
        """Retrieve detailed information about a specific military unit.

        Parameters
        ----------
        mu_id:
            The unique identifier of the military unit.
        """
        return self._post("mu.getById", {"muId": mu_id})

    def get_mus_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        member_id: str | None = None,
        user_id: str | None = None,
        search: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of military units.

        Parameters
        ----------
        limit:
            Maximum number of military units to return (1-100, default 20).
        cursor:
            Pagination cursor for the next page.
        member_id:
            Filter by member ID.
        user_id:
            Filter by user ID.
        search:
            Search query to filter military units.
        """
        return self._post(
            "mu.getManyPaginated",
            _strip_nones({
                "limit": limit,
                "cursor": cursor,
                "memberId": member_id,
                "userId": user_id,
                "search": search,
            }),
        )

    # ── Transaction ──────────────────────────────────────────────────────────

    def get_transactions_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: str | Sequence[str] | None = None,
    ) -> Any:
        """Retrieve a paginated list of transactions.

        Parameters
        ----------
        limit:
            Maximum number of transactions to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        user_id:
            Filter by user ID.
        mu_id:
            Filter by military unit ID.
        country_id:
            Filter by country ID.
        party_id:
            Filter by party ID.
        item_code:
            Filter by item code.
        transaction_type:
            Filter by transaction type(s). Pass a single string or a list
            (see :class:`~warera.enums.TransactionType`).
        """
        body: dict[str, Any] = _strip_nones({
            "limit": limit,
            "cursor": cursor,
            "userId": user_id,
            "muId": mu_id,
            "countryId": country_id,
            "partyId": party_id,
            "itemCode": item_code,
        })
        if transaction_type is not None:
            if isinstance(transaction_type, str):
                body["transactionType"] = transaction_type
            else:
                body["transactionType"] = list(transaction_type)
        return self._post("transaction.getPaginatedTransactions", body)

    # ── Upgrade ──────────────────────────────────────────────────────────────

    def get_upgrade(
        self,
        upgrade_type: str,
        *,
        region_id: str | None = None,
        company_id: str | None = None,
        mu_id: str | None = None,
    ) -> Any:
        """Retrieve upgrade information for a specific type and entity.

        Parameters
        ----------
        upgrade_type:
            The upgrade type to get
            (see :class:`~warera.enums.UpgradeType`).
        region_id:
            The region ID to get the upgrade for.
        company_id:
            The company ID to get the upgrade for.
        mu_id:
            The military unit ID to get the upgrade for.
        """
        body: dict[str, Any] = {"upgradeType": upgrade_type}
        if region_id is not None:
            body["regionId"] = region_id
        if company_id is not None:
            body["companyId"] = company_id
        if mu_id is not None:
            body["muId"] = mu_id
        return self._post("upgrade.getUpgradeByTypeAndEntity", body)

    # ── Worker ───────────────────────────────────────────────────────────────

    def get_workers(
        self,
        *,
        company_id: str | None = None,
        user_id: str | None = None,
    ) -> Any:
        """Get workers for a company or user.

        Parameters
        ----------
        company_id:
            Filter by company ID.
        user_id:
            Filter by user ID.
        """
        return self._post(
            "worker.getWorkers",
            _strip_nones({"companyId": company_id, "userId": user_id}),
        )

    def get_total_workers_count(self, user_id: str) -> Any:
        """Get total workers count for a user.

        Parameters
        ----------
        user_id:
            The unique identifier of the user.
        """
        return self._post("worker.getTotalWorkersCount", {"userId": user_id})


# ═══════════════════════════════════════════════════════════════════════════════
#  Asynchronous client
# ═══════════════════════════════════════════════════════════════════════════════


class AsyncWarEraClient:
    """Asynchronous Python client for the WarEra API.

    Parameters
    ----------
    api_key:
        API key for authentication. Sent as ``X-API-Key`` header.
    base_url:
        Override the default API base URL.
    timeout:
        Request timeout in seconds (default 30).
    **client_kwargs:
        Extra keyword arguments forwarded to :class:`httpx.AsyncClient`.
    """

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = _DEFAULT_BASE_URL,
        timeout: float = 30.0,
        **client_kwargs: Any,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if api_key is not None:
            headers["X-API-Key"] = api_key
        self._client = httpx.AsyncClient(
            base_url=self._base_url,
            timeout=timeout,
            headers=headers,
            **client_kwargs,
        )

    # -- lifecycle -------------------------------------------------------------

    async def close(self) -> None:
        """Close the underlying HTTP transport."""
        await self._client.aclose()

    async def __aenter__(self) -> AsyncWarEraClient:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -- internal --------------------------------------------------------------

    async def _post(self, path: str, body: dict[str, Any] | None = None) -> Any:
        try:
            resp = await self._client.post(f"/{path}", json=body or {})
        except httpx.ConnectError as exc:
            raise WarEraConnectionError(str(exc)) from exc
        return _handle_response(resp)

    # ── Company ──────────────────────────────────────────────────────────────

    async def get_company_by_id(self, company_id: str) -> Any:
        """Retrieve detailed information about a specific company.

        Parameters
        ----------
        company_id:
            The unique identifier of the company.
        """
        return await self._post("company.getById", {"companyId": company_id})

    async def get_companies(
        self,
        *,
        user_id: str | None = None,
        per_page: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of companies.

        Parameters
        ----------
        user_id:
            Filter companies by owner user ID.
        per_page:
            Number of companies per page (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        """
        return await self._post(
            "company.getCompanies",
            _strip_nones({"userId": user_id, "perPage": per_page, "cursor": cursor}),
        )

    # ── Country ──────────────────────────────────────────────────────────────

    async def get_country_by_id(self, country_id: str) -> Any:
        """Retrieve detailed information about a specific country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        """
        return await self._post("country.getCountryById", {"countryId": country_id})

    async def get_all_countries(self) -> Any:
        """Retrieve a list of all available countries."""
        return await self._post("country.getAllCountries")

    # ── Event ────────────────────────────────────────────────────────────────

    async def get_events_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        country_id: str | None = None,
        event_types: Sequence[str] | None = None,
    ) -> Any:
        """Retrieve a paginated list of events.

        Parameters
        ----------
        limit:
            Maximum number of events to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        country_id:
            Filter events by country ID.
        event_types:
            Filter events by event types (use :class:`~warera.enums.EventType`).
        """
        body: dict[str, Any] = _strip_nones({
            "limit": limit,
            "cursor": cursor,
            "countryId": country_id,
        })
        if event_types is not None:
            body["eventTypes"] = list(event_types)
        return await self._post("event.getEventsPaginated", body)

    # ── Government ───────────────────────────────────────────────────────────

    async def get_government_by_country_id(self, country_id: str) -> Any:
        """Retrieve government information for a specific country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        """
        return await self._post("government.getByCountryId", {"countryId": country_id})

    # ── Region ───────────────────────────────────────────────────────────────

    async def get_region_by_id(self, region_id: str) -> Any:
        """Retrieve detailed information about a specific region.

        Parameters
        ----------
        region_id:
            The unique identifier of the region.
        """
        return await self._post("region.getById", {"regionId": region_id})

    async def get_all_regions(self) -> Any:
        """Retrieve a complete object containing all available regions."""
        return await self._post("region.getRegionsObject")

    # ── Battle ───────────────────────────────────────────────────────────────

    async def get_battle_by_id(self, battle_id: str) -> Any:
        """Retrieve detailed information about a specific battle.

        Parameters
        ----------
        battle_id:
            The unique identifier of the battle.
        """
        return await self._post("battle.getById", {"battleId": battle_id})

    async def get_live_battle_data(
        self,
        battle_id: str,
        *,
        round_number: int | None = None,
    ) -> Any:
        """Retrieve real-time battle data including current round information.

        Parameters
        ----------
        battle_id:
            The unique identifier of the battle.
        round_number:
            Optional specific round number to retrieve.
        """
        body: dict[str, Any] = {"battleId": battle_id}
        if round_number is not None:
            body["roundNumber"] = round_number
        return await self._post("battle.getLiveBattleData", body)

    async def get_battles(
        self,
        *,
        is_active: bool | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        direction: str | None = None,
        filter: str | None = None,
        defender_region_id: str | None = None,
        war_id: str | None = None,
        country_id: str | None = None,
    ) -> Any:
        """Retrieve a list of battles.

        Parameters
        ----------
        is_active:
            Whether to get active battles.
        limit:
            Maximum number of battles to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        direction:
            ``"forward"`` or ``"backward"`` (see :class:`~warera.enums.BattleDirection`).
        filter:
            ``"all"``, ``"yourCountry"``, or ``"yourEnemies"``
            (see :class:`~warera.enums.BattleFilter`).
        defender_region_id:
            Filter battles by defender region ID.
        war_id:
            Filter battles by war ID.
        country_id:
            Filter battles by country ID.
        """
        return await self._post(
            "battle.getBattles",
            _strip_nones({
                "isActive": is_active,
                "limit": limit,
                "cursor": cursor,
                "direction": direction,
                "filter": filter,
                "defenderRegionId": defender_region_id,
                "warId": war_id,
                "countryId": country_id,
            }),
        )

    # ── Round ────────────────────────────────────────────────────────────────

    async def get_round_by_id(self, round_id: str) -> Any:
        """Retrieve detailed information about a specific battle round.

        Parameters
        ----------
        round_id:
            The unique identifier of the round.
        """
        return await self._post("round.getById", {"roundId": round_id})

    async def get_last_hits(self, round_id: str) -> Any:
        """Retrieve the most recent hits/damages in a specific battle round.

        Parameters
        ----------
        round_id:
            The unique identifier of the round.
        """
        return await self._post("round.getLastHits", {"roundId": round_id})

    # ── Battle Ranking ───────────────────────────────────────────────────────

    async def get_battle_ranking(
        self,
        *,
        data_type: str,
        type: str,
        side: str,
        battle_id: str | None = None,
        round_id: str | None = None,
        war_id: str | None = None,
    ) -> Any:
        """Retrieve battle rankings.

        Parameters
        ----------
        data_type:
            Type of ranking data: ``"damage"``, ``"points"``, or ``"money"``
            (see :class:`~warera.enums.BattleRankingDataType`).
        type:
            Rank by ``"user"``, ``"country"``, or ``"mu"``
            (see :class:`~warera.enums.BattleRankingType`).
        side:
            ``"attacker"`` or ``"defender"``
            (see :class:`~warera.enums.BattleRankingSide`).
        battle_id:
            Optional battle ID to filter rankings.
        round_id:
            Optional round ID to filter rankings.
        war_id:
            Optional war ID to filter rankings.
        """
        body: dict[str, Any] = {
            "dataType": data_type,
            "type": type,
            "side": side,
        }
        if battle_id is not None:
            body["battleId"] = battle_id
        if round_id is not None:
            body["roundId"] = round_id
        if war_id is not None:
            body["warId"] = war_id
        return await self._post("battleRanking.getRanking", body)

    # ── Item Trading ─────────────────────────────────────────────────────────

    async def get_item_prices(self) -> Any:
        """Retrieve current market prices for all tradeable items."""
        return await self._post("itemTrading.getPrices")

    # ── Trading Order ────────────────────────────────────────────────────────

    async def get_top_orders(
        self,
        item_code: str,
        *,
        limit: int | None = None,
    ) -> Any:
        """Retrieve the best orders for an item.

        Parameters
        ----------
        item_code:
            The item code to get orders for.
        limit:
            Maximum number of orders to return (1-100, default 10).
        """
        body: dict[str, Any] = {"itemCode": item_code}
        if limit is not None:
            body["limit"] = limit
        return await self._post("tradingOrder.getTopOrders", body)

    # ── Item Offer ───────────────────────────────────────────────────────────

    async def get_item_offer_by_id(self, item_offer_id: str) -> Any:
        """Retrieve detailed information about a specific item offer.

        Parameters
        ----------
        item_offer_id:
            The unique identifier of the item offer.
        """
        return await self._post("itemOffer.getById", {"itemOfferId": item_offer_id})

    # ── Work Offer ───────────────────────────────────────────────────────────

    async def get_work_offer_by_id(self, work_offer_id: str) -> Any:
        """Retrieve detailed information about a specific work offer.

        Parameters
        ----------
        work_offer_id:
            The unique identifier of the work offer.
        """
        return await self._post("workOffer.getById", {"workOfferId": work_offer_id})

    async def get_work_offer_by_company_id(self, company_id: str) -> Any:
        """Retrieve the work offer for a specific company.

        Parameters
        ----------
        company_id:
            The unique identifier of the company.
        """
        return await self._post("workOffer.getWorkOfferByCompanyId", {"companyId": company_id})

    async def get_work_offers_paginated(
        self,
        *,
        user_id: str | None = None,
        region_id: str | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        energy: float | None = None,
        production: float | None = None,
        citizenship: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of work offers.

        Parameters
        ----------
        user_id:
            Filter by user ID.
        region_id:
            Filter by region ID.
        cursor:
            Pagination cursor for the next page.
        limit:
            Number of work offers per page (default 10).
        energy:
            Minimum energy filter (>= 0).
        production:
            Minimum production filter (>= 0).
        citizenship:
            Filter by citizenship country.
        """
        return await self._post(
            "workOffer.getWorkOffersPaginated",
            _strip_nones({
                "userId": user_id,
                "regionId": region_id,
                "cursor": cursor,
                "limit": limit,
                "energy": energy,
                "production": production,
                "citizenship": citizenship,
            }),
        )

    # ── Ranking ──────────────────────────────────────────────────────────────

    async def get_ranking(self, ranking_type: str) -> Any:
        """Retrieve ranking data for the specified ranking type.

        Parameters
        ----------
        ranking_type:
            The type of ranking to retrieve
            (see :class:`~warera.enums.RankingType`).
        """
        return await self._post("ranking.getRanking", {"rankingType": ranking_type})

    # ── Search ───────────────────────────────────────────────────────────────

    async def search(self, search_text: str) -> Any:
        """Perform a global search across all entities.

        Parameters
        ----------
        search_text:
            The search query string.
        """
        return await self._post("search.searchAnything", {"searchText": search_text})

    # ── Game Config ──────────────────────────────────────────────────────────

    async def get_game_dates(self) -> Any:
        """Retrieve game-related dates and timings."""
        return await self._post("gameConfig.getDates")

    async def get_game_config(self) -> Any:
        """Retrieve the static game configuration."""
        return await self._post("gameConfig.getGameConfig")

    # ── User ─────────────────────────────────────────────────────────────────

    async def get_user_lite(self, user_id: str) -> Any:
        """Retrieve basic public information about a user.

        Parameters
        ----------
        user_id:
            The unique identifier of the user.
        """
        return await self._post("user.getUserLite", {"userId": user_id})

    async def get_users_by_country(
        self,
        country_id: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
    ) -> Any:
        """Retrieve a list of users by country.

        Parameters
        ----------
        country_id:
            The unique identifier of the country.
        limit:
            Maximum number of users to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        """
        body: dict[str, Any] = {"countryId": country_id}
        if limit is not None:
            body["limit"] = limit
        if cursor is not None:
            body["cursor"] = cursor
        return await self._post("user.getUsersByCountry", body)

    # ── Article ──────────────────────────────────────────────────────────────

    async def get_article_by_id(self, article_id: str) -> Any:
        """Retrieve detailed information about a specific article.

        Parameters
        ----------
        article_id:
            The ID of the article to get.
        """
        return await self._post("article.getArticleById", {"articleId": article_id})

    async def get_article_lite_by_id(self, article_id: str) -> Any:
        """Retrieve only the title and basic stats of an article (no view counted).

        Parameters
        ----------
        article_id:
            The ID of the article to get.
        """
        return await self._post("article.getArticleLiteById", {"articleId": article_id})

    async def get_articles_paginated(
        self,
        type: str,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        user_id: str | None = None,
        categories: Sequence[str] | None = None,
        languages: Sequence[str] | None = None,
        positive_score_only: bool | None = None,
    ) -> Any:
        """Retrieve a paginated list of articles.

        Parameters
        ----------
        type:
            The type of articles to get: ``"daily"``, ``"weekly"``, ``"top"``,
            ``"my"``, ``"subscriptions"``, or ``"last"``
            (see :class:`~warera.enums.ArticleListType`).
        limit:
            Maximum number of articles to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        user_id:
            The user ID to get articles for.
        categories:
            Filter by article categories.
        languages:
            Filter by article languages.
        positive_score_only:
            Only show articles with a positive score.
        """
        body: dict[str, Any] = {"type": type}
        body.update(_strip_nones({
            "limit": limit,
            "cursor": cursor,
            "userId": user_id,
            "positiveScoreOnly": positive_score_only,
        }))
        if categories is not None:
            body["categories"] = list(categories)
        if languages is not None:
            body["languages"] = list(languages)
        return await self._post("article.getArticlesPaginated", body)

    # ── Military Unit (MU) ───────────────────────────────────────────────────

    async def get_mu_by_id(self, mu_id: str) -> Any:
        """Retrieve detailed information about a specific military unit.

        Parameters
        ----------
        mu_id:
            The unique identifier of the military unit.
        """
        return await self._post("mu.getById", {"muId": mu_id})

    async def get_mus_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        member_id: str | None = None,
        user_id: str | None = None,
        search: str | None = None,
    ) -> Any:
        """Retrieve a paginated list of military units.

        Parameters
        ----------
        limit:
            Maximum number of military units to return (1-100, default 20).
        cursor:
            Pagination cursor for the next page.
        member_id:
            Filter by member ID.
        user_id:
            Filter by user ID.
        search:
            Search query to filter military units.
        """
        return await self._post(
            "mu.getManyPaginated",
            _strip_nones({
                "limit": limit,
                "cursor": cursor,
                "memberId": member_id,
                "userId": user_id,
                "search": search,
            }),
        )

    # ── Transaction ──────────────────────────────────────────────────────────

    async def get_transactions_paginated(
        self,
        *,
        limit: int | None = None,
        cursor: str | None = None,
        user_id: str | None = None,
        mu_id: str | None = None,
        country_id: str | None = None,
        party_id: str | None = None,
        item_code: str | None = None,
        transaction_type: str | Sequence[str] | None = None,
    ) -> Any:
        """Retrieve a paginated list of transactions.

        Parameters
        ----------
        limit:
            Maximum number of transactions to return (1-100, default 10).
        cursor:
            Pagination cursor for the next page.
        user_id:
            Filter by user ID.
        mu_id:
            Filter by military unit ID.
        country_id:
            Filter by country ID.
        party_id:
            Filter by party ID.
        item_code:
            Filter by item code.
        transaction_type:
            Filter by transaction type(s). Pass a single string or a list
            (see :class:`~warera.enums.TransactionType`).
        """
        body: dict[str, Any] = _strip_nones({
            "limit": limit,
            "cursor": cursor,
            "userId": user_id,
            "muId": mu_id,
            "countryId": country_id,
            "partyId": party_id,
            "itemCode": item_code,
        })
        if transaction_type is not None:
            if isinstance(transaction_type, str):
                body["transactionType"] = transaction_type
            else:
                body["transactionType"] = list(transaction_type)
        return await self._post("transaction.getPaginatedTransactions", body)

    # ── Upgrade ──────────────────────────────────────────────────────────────

    async def get_upgrade(
        self,
        upgrade_type: str,
        *,
        region_id: str | None = None,
        company_id: str | None = None,
        mu_id: str | None = None,
    ) -> Any:
        """Retrieve upgrade information for a specific type and entity.

        Parameters
        ----------
        upgrade_type:
            The upgrade type to get
            (see :class:`~warera.enums.UpgradeType`).
        region_id:
            The region ID to get the upgrade for.
        company_id:
            The company ID to get the upgrade for.
        mu_id:
            The military unit ID to get the upgrade for.
        """
        body: dict[str, Any] = {"upgradeType": upgrade_type}
        if region_id is not None:
            body["regionId"] = region_id
        if company_id is not None:
            body["companyId"] = company_id
        if mu_id is not None:
            body["muId"] = mu_id
        return await self._post("upgrade.getUpgradeByTypeAndEntity", body)

    # ── Worker ───────────────────────────────────────────────────────────────

    async def get_workers(
        self,
        *,
        company_id: str | None = None,
        user_id: str | None = None,
    ) -> Any:
        """Get workers for a company or user.

        Parameters
        ----------
        company_id:
            Filter by company ID.
        user_id:
            Filter by user ID.
        """
        return await self._post(
            "worker.getWorkers",
            _strip_nones({"companyId": company_id, "userId": user_id}),
        )

    async def get_total_workers_count(self, user_id: str) -> Any:
        """Get total workers count for a user.

        Parameters
        ----------
        user_id:
            The unique identifier of the user.
        """
        return await self._post("worker.getTotalWorkersCount", {"userId": user_id})
