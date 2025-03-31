from dataclasses import dataclass

import httpx


@dataclass
class YandexClient:
    async_client: httpx.AsyncClient
