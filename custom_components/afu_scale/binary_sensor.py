"""AFU 体脂秤"测量中"二进制传感器"""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import AfuScaleCoordinator


class AfuMeasuringBinarySensor(BinarySensorEntity):
    """测量中：收到体重数据即开，无数据 15 秒后自动关。"""

    def __init__(self, coordinator: AfuScaleCoordinator) -> None:
        self._coordinator = coordinator
        self._attr_unique_id = f"{DOMAIN}_{coordinator.address}_measuring"
        self._attr_name = "AFU 体脂秤测量中"
        self._attr_device_class = BinarySensorDeviceClass.MOTION
        self._attr_should_poll = False
        self._attr_icon = "mdi:scale-bathroom"

    @property
    def device_info(self) -> DeviceInfo:
        return DeviceInfo(
            identifiers={(DOMAIN, self._coordinator.address)},
            name="AFU 体脂秤",
            manufacturer="沃莱科技",
            model="AFU-WL-TZ-A1",
        )

    @callback
    def async_update_state(self, value: bool) -> None:
        self._attr_is_on = value
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator: AfuScaleCoordinator = hass.data[DOMAIN][entry.entry_id]
    entity = AfuMeasuringBinarySensor(coordinator)
    async_add_entities([entity])
    coordinator.measuring_entity = entity
    if coordinator.measuring:
        entity.async_update_state(True)
