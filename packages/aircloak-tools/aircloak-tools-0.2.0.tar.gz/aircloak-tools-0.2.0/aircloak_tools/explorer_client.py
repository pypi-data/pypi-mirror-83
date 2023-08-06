import logging
import os
import requests
import time

from typing import List, Dict, Optional

logger = logging.Logger(__name__)


class ExplorerError(RuntimeError):
    pass


class ExplorerSession:
    API_VERSION = "v1"

    def __init__(self, base_url: str, port: int, aircloak_api_url: str, api_key: str):
        self.explorer_api_url = f'{base_url}:{port}/api/{self.API_VERSION}'
        self.aircloak_api_url = aircloak_api_url
        self.api_key = api_key

    def _post_explore(self, dataset: str, table: str, columns: List[str]) -> str:
        logger.debug(
            f'POSTing to /explore for {dataset}:{table}:{columns}.')

        response = requests.post(
            f"{self.explorer_api_url}/explore",
            json={
                "ApiUrl": self.aircloak_api_url,
                "ApiKey": self.api_key,
                "DataSource": dataset,
                "Table": table,
                "Columns": columns,
            },
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            logger.warning(
                f"Http Error {response.status_code}: {response.json()}")

        body = response.json()

        if 'id' not in body:
            raise ExplorerError(response)

        logger.debug(
            f'Polling results for exploration "{body["id"]}".')

        return body['id']

    def _poll_get_result(self, id: str, timeout: int = 10 * 60):
        poll_count: int = 0
        poll_interval: int = 1
        poll_max_interval: int = 2 ** 3
        slept: int = 0

        logger.debug(
            f'Polling results for exploration "{id}".')

        while slept < timeout:
            poll_count += 1
            logger.debug(f"polling...{poll_count}")

            response = requests.get(f"{self.explorer_api_url}/result/{id}")
            response.raise_for_status()

            status = response.json()["status"]
            if status in ["Complete", "Error"]:
                logger.debug(
                    f'Polling complete, exploration status: "{status}"')
                return response.json()
            else:
                logger.debug(f'status is "{status}"')

            if poll_interval <= poll_max_interval:
                poll_interval *= 2

            time.sleep(poll_interval)
            slept += poll_interval

        raise TimeoutError(response)


class Exploration:
    def __init__(self, session: ExplorerSession, dataset: str, table: str, columns: List[str]):
        self.dataset = dataset
        self.table = table
        self.columns = columns
        self.session = session

        self.cache_id: str = '/'.join([session.aircloak_api_url, dataset, table,
                                       '+'.join(columns)])

    def explore(self, refresh_cache: bool):
        if (refresh_cache or self.cache_entry is None):
            try:
                id = self.session._post_explore(
                    self.dataset, self.table, self.columns)
            except ExplorerError as err:
                self.log_and_raise_error(
                    f"Unable to launch exploration.\n{err}")

            try:
                result = self.session._poll_get_result(id)
            except TimeoutError as err:
                self.log_and_raise_error(f"Explorer request timed out.\n{err}")

            if result["status"] == "Error":
                self.log_and_raise_error(
                    f"Internal Explorer error: {result['description']}.")

            self.cache_entry = result
        else:
            logger.info("Pulling response json from cache.")

        return self.cache_entry

    # RESPONSE CACHE #
    RESPONSE_CACHE: Dict[str, Dict] = {}

    @property
    def cache_entry(self) -> Optional[Dict]:
        try:
            return Exploration.RESPONSE_CACHE[self.cache_id]
        except KeyError:
            return None

    @cache_entry.setter
    def cache_entry(self, value):
        Exploration.RESPONSE_CACHE[self.cache_id] = value

    @cache_entry.deleter
    def cache_entry(self):
        del Exploration.RESPONSE_CACHE[self.cache_id]

    @classmethod
    def clear_cache(cls):
        cls.RESPONSE_CACHE = {}

    def log_and_raise_error(self, msg: str):
        logger.error(msg)
        raise ExplorerError(self)
