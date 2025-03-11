"""Update coordinator for bafavorank."""
import logging
from typing import Callable
from datetime import timedelta
import async_timeout

from homeassistant import core
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .utils import get_total_rank

_LOGGER = logging.getLogger(__name__)


class BafavorankDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching bafavorank data."""

    def __init__(self, hass: core.HomeAssistant, config: dict) -> None:
        """Initialize."""
        self.hass = hass
        self.config = config
        self.url = config["url"]
        self.access_token = config["access_token"]
        self.usercode = config["usercode"]
        self.stuid = config["stuid"]
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{self.usercode}_{self.stuid}",
            update_interval=timedelta(hours=3),
            always_update=False
        )
    
    async def _async_update_data(self) -> int:
        """Fetch data from arona.icu."""
        try:
            async with async_timeout.timeout(10):
                session = async_get_clientsession(self.hass)
                resp = await session.post(
                    self.url,
                    json={"friend": self.usercode},
                    headers={"Authorization": self.access_token},
                )
                response = await resp.json()
                total_rank = -1
                if response["code"] == 4003:
                    _LOGGER.warning("token quota exceeded")
                    return self.data
                for assist in response["data"]["assistInfoList"]:
                    if assist["uniqueId"] == self.stuid:
                        total_rank = get_total_rank(assist["favorRank"], assist["favorExp"])
                        break
                if total_rank == -1:
                    raise ValueError("Student not found")
                return total_rank
        except Exception as e:
            _LOGGER.error("Error: %s", e)
            return self.data