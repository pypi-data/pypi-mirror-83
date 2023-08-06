from contextlib import contextmanager
from typing import Iterator

from .aircloak_client import AircloakConnection


@contextmanager
def connect(host, port, user, password, dataset) -> Iterator[AircloakConnection]:
    try:
        ac = AircloakConnection(
            host=host, port=port, user=user, password=password, dataset=dataset)
        yield ac
    finally:
        ac.close()
