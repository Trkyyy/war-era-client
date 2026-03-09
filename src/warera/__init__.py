"""warera — Python client for the WarEra game API.

Quick-start::

    from warera import WarEraClient

    client = WarEraClient()
    countries = client.get_all_countries()

For async usage::

    from warera import AsyncWarEraClient

    async with AsyncWarEraClient() as client:
        countries = await client.get_all_countries()
"""

from warera.client import AsyncWarEraClient, WarEraClient
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
from warera.exceptions import WarEraAPIError, WarEraConnectionError, WarEraError

__all__ = [
    # clients
    "WarEraClient",
    "AsyncWarEraClient",
    # enums
    "ArticleListType",
    "BattleDirection",
    "BattleFilter",
    "BattleRankingDataType",
    "BattleRankingSide",
    "BattleRankingType",
    "EventType",
    "RankingType",
    "TransactionType",
    "UpgradeType",
    # exceptions
    "WarEraError",
    "WarEraAPIError",
    "WarEraConnectionError",
]
