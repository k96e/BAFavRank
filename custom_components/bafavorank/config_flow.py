import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN, CONF_USERCODE, CONF_STUID, DICT_STU
from .utils import get_stu_id, get_stu_name

_LOGGER = logging.getLogger(__name__)

AUTH_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_URL,default="https://api.arona.icu/api/friends/refresh"): cv.string,
        vol.Required(CONF_ACCESS_TOKEN): cv.string, 
        vol.Required(CONF_USERCODE): cv.string
    }
)
SELE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_STUID): cv.string,
    }
)

cached_resp = None

async def validate_auth(user_input: Dict[str, Any], hass: core.HomeAssistant) -> None:
    """Validates a arona.icu auth.

    Raises a ValueError if invalid.
    """
    global cached_resp
    session = async_get_clientsession(hass)
    try:
        if not cached_resp:
            resp = await session.post(
                user_input[CONF_URL],
                json={"friend": user_input[CONF_USERCODE]},
                headers={"Authorization": user_input[CONF_ACCESS_TOKEN]},
            )
            response = await resp.json()
            _LOGGER.info("Response: %s", response)
            cached_resp = response
        else:
            response = cached_resp
            _LOGGER.info("Cached response: %s", response)
        assert response["message"] == "success" and response["crypt"] == False
        return response
    except Exception as e:
        _LOGGER.error("Error: %s", e)
        raise ValueError


async def validate_select(user_input: Dict[str, Any], response:Dict[str, Any], hass: core.HomeAssistant) -> None:
    """Validates selected student.

    Raises a ValueError if invalid.
    """
    try:
        stu = get_stu_id(user_input[CONF_STUID])
        for assist in response["data"]["assistInfoList"]:
            if assist["uniqueId"] == stu:
                return
        raise ValueError
    except Exception:
        raise ValueError

class BAConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Blue Archive favor rank custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            try:
                self.temp_resp = await validate_auth(user_input, self.hass)
            except ValueError:
                errors["base"] = "auth"
            if not errors:
                # Input is valid, set data.
                self.data = user_input
                # Return the form of the next step.
                return await self.async_step_select()

        return self.async_show_form(
            step_id="user", data_schema=AUTH_SCHEMA, errors=errors
        )

    async def async_step_select(self, user_input: Optional[Dict[str, Any]] = None):
        """Second step in config flow to select a student to watch."""
        errors: Dict[str, str] = {}
        if user_input is not None:
            # Validate the path.
            try:
                await validate_select(user_input, self.temp_resp, self.hass)
            except ValueError:
                errors["base"] = "no_student"

            if not errors:
                _LOGGER.info(user_input)
                self.data[CONF_STUID] = get_stu_id(user_input[CONF_STUID])
                _LOGGER.info(self.data)
                return self.async_create_entry(title=f"{self.data['usercode']}_{get_stu_name(self.data['stuid'])}", data=self.data)
        options = []
        for stu in self.temp_resp["data"]["assistInfoList"]:
            options.append(DICT_STU.get(stu["uniqueId"], f"{stu['uniqueId']}"))
        return self.async_show_form(
            step_id="select", data_schema=vol.Schema({
                vol.Required(CONF_STUID): vol.In(options)
            }), errors=errors
        )