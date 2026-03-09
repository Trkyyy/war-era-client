# warera

Python client for the [WarEra](https://warera.io) game API (`https://api2.warera.io`).

Provides both **synchronous** and **asynchronous** clients with a method for every public API endpoint.

## Installation

```bash
pip install .
```

Or install directly from the repo:

```bash
pip install git+https://github.com/Trkyyy/war-era-client.git
```

## Quick start

### Synchronous

```python
from warera import WarEraClient

client = WarEraClient("your-api-key")

# Get all countries
countries = client.get_all_countries()

# Look up a user
user = client.get_user_lite(user_id="some-user-id")

# Get active battles
battles = client.get_battles(is_active=True, limit=5)

# Don't forget to close when done (or use a context manager)
client.close()
```

### Context manager

```python
from warera import WarEraClient

with WarEraClient("your-api-key") as client:
    config = client.get_game_config()
    print(config)
```

### Async

```python
import asyncio
from warera import AsyncWarEraClient

async def main():
    async with AsyncWarEraClient("your-api-key") as client:
        prices = await client.get_item_prices()
        print(prices)

asyncio.run(main())
```

## Authentication

The API uses an `X-API-Key` header. Pass your key as the first argument:

```python
client = WarEraClient("your-api-key")
```

The key can also be loaded from an environment variable:

```python
import os
from warera import WarEraClient

client = WarEraClient(os.environ["WARERA_API_KEY"])
```

If no key is provided, requests are sent without the header (useful for
unauthenticated endpoints).

## Available methods

Every public endpoint from the [WarEra API docs](https://api2.warera.io/docs) is mapped to a client method:

| Method | Description |
|---|---|
| `get_company_by_id(company_id)` | Get company by ID |
| `get_companies(*, user_id, per_page, cursor)` | Get companies (paginated) |
| `get_country_by_id(country_id)` | Get country by ID |
| `get_all_countries()` | Get all countries |
| `get_events_paginated(*, limit, cursor, country_id, event_types)` | Get paginated events |
| `get_government_by_country_id(country_id)` | Get government by country ID |
| `get_region_by_id(region_id)` | Get region by ID |
| `get_all_regions()` | Get all regions |
| `get_battle_by_id(battle_id)` | Get battle by ID |
| `get_live_battle_data(battle_id, *, round_number)` | Get live battle data |
| `get_battles(*, is_active, limit, cursor, direction, filter, ...)` | Get battles |
| `get_round_by_id(round_id)` | Get round by ID |
| `get_last_hits(round_id)` | Get last hits in a round |
| `get_battle_ranking(*, data_type, type, side, battle_id, ...)` | Get battle rankings |
| `get_item_prices()` | Get item market prices |
| `get_top_orders(item_code, *, limit)` | Get best orders for an item |
| `get_item_offer_by_id(item_offer_id)` | Get item offer by ID |
| `get_work_offer_by_id(work_offer_id)` | Get work offer by ID |
| `get_work_offer_by_company_id(company_id)` | Get work offer by company ID |
| `get_work_offers_paginated(*, user_id, region_id, cursor, ...)` | Get work offers (paginated) |
| `get_ranking(ranking_type)` | Get ranking data |
| `search(search_text)` | Global search |
| `get_game_dates()` | Get game dates |
| `get_game_config()` | Get game configuration |
| `get_user_lite(user_id)` | Get user profile (lite) |
| `get_users_by_country(country_id, *, limit, cursor)` | Get users by country |
| `get_article_by_id(article_id)` | Get article by ID |
| `get_article_lite_by_id(article_id)` | Get article lite by ID |
| `get_articles_paginated(type, *, limit, cursor, user_id, ...)` | Get articles (paginated) |
| `get_mu_by_id(mu_id)` | Get military unit by ID |
| `get_mus_paginated(*, limit, cursor, member_id, user_id, ...)` | Get military units (paginated) |
| `get_transactions_paginated(*, limit, cursor, user_id, ...)` | Get transactions (paginated) |
| `get_upgrade(upgrade_type, *, region_id, company_id, mu_id)` | Get upgrade info |
| `get_workers(*, company_id, user_id)` | Get workers |
| `get_total_workers_count(user_id)` | Get total workers count |

## Enums

The package ships convenience `StrEnum` constants so you never have to hard-code string values:

```python
from warera import RankingType, EventType

client.get_ranking(RankingType.USER_LEVEL)
client.get_events_paginated(event_types=[EventType.WAR_DECLARED, EventType.BATTLE_OPENED])
```

Available enums: `EventType`, `BattleDirection`, `BattleFilter`, `BattleRankingDataType`, `BattleRankingType`, `BattleRankingSide`, `RankingType`, `ArticleListType`, `TransactionType`, `UpgradeType`.

## Error handling

```python
from warera import WarEraClient, WarEraAPIError, WarEraConnectionError

client = WarEraClient()

try:
    user = client.get_user_lite(user_id="invalid")
except WarEraAPIError as e:
    print(f"HTTP {e.status_code}: {e.detail}")
except WarEraConnectionError:
    print("Could not reach the API")
```

## Configuration

```python
# Custom base URL and timeout
client = WarEraClient(
    "your-api-key",
    base_url="https://api2.warera.io/trpc",
    timeout=60.0,
)
```

## License

MIT
