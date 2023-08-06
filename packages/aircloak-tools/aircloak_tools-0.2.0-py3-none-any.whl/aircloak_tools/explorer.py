import os

from typing import List, Dict

from aircloak_tools.explorer_client import ExplorerSession, Exploration

API_KEY = os.environ["AIRCLOAK_API_KEY"]
ATTACK_SERVER_API_URL = "https://attack.aircloak.com/api"
EXPLORER_DEFAULT_URL = "http://localhost"
EXPLORER_DEFAULT_PORT = 5000


def explorer_session(
        base_url: str = EXPLORER_DEFAULT_URL,
        port: int = EXPLORER_DEFAULT_PORT,
        aircloak_api_url: str = ATTACK_SERVER_API_URL,
        api_key: str = API_KEY) -> ExplorerSession:

    return ExplorerSession(base_url, port, aircloak_api_url, api_key)


def explore(
        session: ExplorerSession,
        dataset: str,
        table: str,
        columns: List[str],
        refresh_cache: bool = False) -> Dict:

    return Exploration(session, dataset, table, columns).explore(refresh_cache)
