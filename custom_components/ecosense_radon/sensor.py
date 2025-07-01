from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

RADON_CONCENTRATION_PICOCURIES_PER_LITER = "pCi/L"
RADON_UNIT_CONVERSION_SCALE = 37.0

SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="radon_level",
        name="Radon Level",
        native_unit_of_measurement=RADON_CONCENTRATION_PICOCURIES_PER_LITER,
        state_class=SensorStateClass.MEASUREMENT,
    ),
    SensorEntityDescription(
        key="alert_level",
        name="Alert Level",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: DataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []
    if coordinator.data:
        for device_data in coordinator.data:
            for description in SENSORS:
                entities.append(
                    EcoSenseRadonSensor(coordinator, device_data, description)
                )

    async_add_entities(entities)


class EcoSenseRadonSensor(CoordinatorEntity, SensorEntity):
    """Represents an EcoSense Radon sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device_data: dict,
        description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._serial_number = device_data["serial_number"]

        self._attr_unique_id = f"{self._serial_number}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._serial_number)},
            name=device_data.get("device_name", "EcoSense Radon Monitor"),
            manufacturer="Ecosense",
            model=device_data.get("device_name"),
            sw_version=device_data.get("fw_version"),
        )

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self.entity_description.key != "alert_level":
            return self.entity_description.icon

        state = self.native_value
        if state == "Green":
            return "mdi:shield-check-outline"
        if state == "Orange":
            return "mdi:shield-alert-outline"
        if state == "Red":
            return "mdi:shield-alert"
        return "mdi:shield-off-outline"

    @property
    def icon_color(self) -> str | None:
        """Return the icon color based on the alert level."""
        if self.entity_description.key != "alert_level":
            return None

        state = self.native_value
        if state == "Green":
            return "green"
        if state == "Orange":
            return "orange"
        if state == "Red":
            return "red"
        return None

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes, including rgb_color for alert_level."""
        if self.entity_description.key != "alert_level":
            return {}

        rgb_map: dict[str, tuple[int, int, int]] = {
            "Green": (0, 200, 83),  # #00c853
            "Orange": (255, 171, 0),  # #ffab00
            "Red": (213, 0, 0),  # #d50000
        }
        rgb = rgb_map.get(self.native_value)
        return {"rgb_color": rgb} if rgb else {}

    @property
    def _device_data(self) -> dict | None:
        """Return this sensor's device data from the coordinator."""
        if not self.coordinator.data:
            return None
        for device in self.coordinator.data:
            if device.get("serial_number") == self._serial_number:
                return device
        return None

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if (device_data := self._device_data) is None:
            return None

        key = self.entity_description.key

        if key == "radon_level":
            try:
                value = device_data["radon_level"]
                return round(float(value) / RADON_UNIT_CONVERSION_SCALE, 1)
            except (KeyError, ValueError, TypeError):
                return None

        if key == "alert_level":
            try:
                radon_level = float(device_data["radon_level"])
                config = device_data["config"]
                level2 = float(config["level2"])
                level3 = float(config["level3"])
            except (KeyError, TypeError, ValueError):
                return None

            if radon_level < level2:
                return "Green"
            if radon_level < level3:
                return "Orange"
            return "Red"

        return device_data.get(key)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return super().available and self._device_data is not None
