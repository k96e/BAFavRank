"""bafavrank sensor platform."""
import logging
from typing import Any, Dict, Optional

from homeassistant import core, config_entries
from homeassistant.core import callback
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .utils import get_stu_name, get_level_by_rank, get_total_rank
from .update_coordinator import BafavorankDataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = config_entry.data
    _LOGGER.info("Setting up sensor for %s", config)

    coordinator = BafavorankDataUpdateCoordinator(hass, config)
    await coordinator.async_config_entry_first_refresh()

    sensors = [
        RankSensor(hass, config, coordinator),
        ExpSensor(hass, config, coordinator),
        LevelExpSensor(hass, config, coordinator),
        LevelRemainExpSensor(hass, config, coordinator),
        HundredRankSensor(hass, config, coordinator)
    ]
    async_add_entities(sensors, update_before_add=True)

class RankSensor(CoordinatorEntity, SensorEntity):
    """Current rank sensor. (1 to 100)"""

    def __init__(self, hass: core.HomeAssistant, config: Dict[str, Any], coordinator) -> None:
        """Initialize the sensor."""
        self._config = config
        self._hass = hass
        self.coordinator = coordinator
        self._attr_unique_id = f"{config['usercode']}_{config['stuid']}_rank"
        self.entity_id = f"sensor.{config['usercode']}_{config['stuid']}_rank"
        self._attr_name = f"{get_stu_name(config['stuid'])} 的好感等级"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:heart"
        self._attr_state_class = SensorStateClass.TOTAL
        super().__init__(coordinator)

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        value = get_level_by_rank(self.coordinator.data)[0]
        return value

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = get_level_by_rank(self.coordinator.data)[0]
        self._attr_native_value = value
        self.async_write_ha_state()

class ExpSensor(CoordinatorEntity, SensorEntity):
    """Current favor exp sensor. (240225 max)"""

    def __init__(self, hass: core.HomeAssistant, config: Dict[str, Any], coordinator) -> None:
        """Initialize the sensor."""
        self._config = config
        self._hass = hass
        self.coordinator = coordinator
        self._attr_unique_id = f"{config['usercode']}_{config['stuid']}_exp"
        self.entity_id = f"sensor.{config['usercode']}_{config['stuid']}_exp"
        self._attr_name = f"{get_stu_name(config['stuid'])} 的好感经验"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:heart"
        self._attr_state_class = SensorStateClass.TOTAL
        super().__init__(coordinator)

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        value = self.coordinator.data
        return value
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = self.coordinator.data
        self._attr_native_value = value
        self.async_write_ha_state()

class LevelExpSensor(CoordinatorEntity, SensorEntity):
    """Exp of current favor level sensor."""

    def __init__(self, hass: core.HomeAssistant, config: Dict[str, Any], coordinator) -> None:
        """Initialize the sensor."""
        self._config = config
        self._hass = hass
        self.coordinator = coordinator
        self._attr_unique_id = f"{config['usercode']}_{config['stuid']}_level_exp"
        self.entity_id = f"sensor.{config['usercode']}_{config['stuid']}_level_exp"
        self._attr_name = f"{get_stu_name(config['stuid'])} 的当前好感等级经验"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:heart"
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        super().__init__(coordinator)

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        value = get_level_by_rank(self.coordinator.data)[1]
        return value
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = get_level_by_rank(self.coordinator.data)[1]
        self._attr_native_value = value
        self.async_write_ha_state()

class LevelRemainExpSensor(CoordinatorEntity, SensorEntity):
    """Exp needed to next favor level sensor."""

    def __init__(self, hass: core.HomeAssistant, config: Dict[str, Any], coordinator) -> None:
        """Initialize the sensor."""
        self._config = config
        self._hass = hass
        self.coordinator = coordinator
        self._attr_unique_id = f"{config['usercode']}_{config['stuid']}_level_remain_exp"
        self.entity_id = f"sensor.{config['usercode']}_{config['stuid']}_level_remain_exp"
        self._attr_name = f"{get_stu_name(config['stuid'])} 升级还需经验"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:heart"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        super().__init__(coordinator)

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        level = get_level_by_rank(self.coordinator.data)[0]
        if level >= 100:
            return 0
        next_exp = get_total_rank(level+1, 0)
        return next_exp - self.coordinator.data
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        level = get_level_by_rank(self.coordinator.data)[0]
        if level >= 100:
            self._attr_native_value = 0
        else:
            next_exp = get_total_rank(level + 1, 0)
            self._attr_native_value = next_exp - self.coordinator.data
        self.async_write_ha_state()

class HundredRankSensor(CoordinatorEntity, SensorEntity):
    """Persentage of current rank to 100 sensor."""

    def __init__(self, hass: core.HomeAssistant, config: Dict[str, Any], coordinator) -> None:
        """Initialize the sensor."""
        self._config = config
        self._hass = hass
        self.coordinator = coordinator
        self._attr_unique_id = f"{config['usercode']}_{config['stuid']}_hundred_percent"
        self.entity_id = f"sensor.{config['usercode']}_{config['stuid']}_hundred_percent"
        self._attr_name = f"{get_stu_name(config['stuid'])} 的百绊进度"
        self._attr_has_entity_name = True
        self._attr_icon = "mdi:heart"
        self._attr_native_unit_of_measurement = "%"
        self._attr_suggested_display_precision = 4
        self._attr_state_class = SensorStateClass.TOTAL
        super().__init__(coordinator)

    @property
    def native_value(self) -> Optional[int]:
        """Return the state of the sensor."""
        value = round(int(self.coordinator.data) / 240225 * 100, 4)
        return value
    
    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        value = round(int(self.coordinator.data) / 240225 * 100, 4)
        self._attr_native_value = value
        self.async_write_ha_state()