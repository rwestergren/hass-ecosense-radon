# EcoSense Radon – Home Assistant Integration

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rwestergren&repository=hass-ecosense-radon&category=integration)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg?style=flat-square)](https://hacs.xyz/) [![GitHub issues](https://img.shields.io/github/issues/rwestergren/hass-ecosense-radon?style=flat-square)](https://github.com/rwestergren/hass-ecosense-radon/issues)

This custom integration connects EcoSense cloud-connected radon monitors to Home Assistant, providing current radon readings and alert levels.

## Features

- Radon Level sensor with configurable units (`pCi/L` or `Bq/m³`)
- Alert Level sensor (Green / Orange / Red) with EPA-based thresholds
- Device info and automatic cloud polling every 5 minutes
- Unit configuration during setup and changeable via integration options

## Installation

### **Quick install with My Home Assistant**

1. Click the badge at the top of this README.  
2. Your Home Assistant will open with the repository pre-selected in HACS.  
3. Follow the prompts to install and then restart Home Assistant.

### **HACS (custom repository)**

1. In HACS, go to **Integrations → Custom repositories** and add this repository URL as **Integration**.  
2. Search for "EcoSense Radon" in HACS and install it.  
3. Restart Home Assistant.

### **Manual**

Copy the `custom_components/ecosense_radon/` folder into your Home Assistant `custom_components/` directory and restart Home Assistant.

## Configuration

1. Go to **Settings** > **Devices & Services** in Home Assistant.
2. Click **Add Integration** and search for "EcoSense Radon".
3. Enter your EcoSense cloud username and password when prompted.
4. Select your preferred radon unit:
   - **pCi/L** (Picocuries per Liter) - Default
   - **Bq/m³** (Becquerels per Cubic Meter)

### Changing Units After Setup

You can change the radon unit at any time:
1. Go to **Settings** > **Devices & Services**
2. Find your EcoSense Radon integration
3. Click **Configure**
4. Select your preferred unit and click **Submit**

## Entities Created

| Entity ID suffix | Description         | Unit          |
|------------------|---------------------|---------------|
| `radon_level`    | Radon Level         | pCi/L or Bq/m³|
| `alert_level`    | Alert Level (status)| —             |

## Alert Level Thresholds

The alert level sensor uses EPA-recommended thresholds that automatically adjust based on your selected unit:

### pCi/L (Picocuries per Liter)
- **Green**: < 2.7 pCi/L
- **Orange**: 2.7 - 4.0 pCi/L (EPA recommends considering mitigation)
- **Red**: > 4.0 pCi/L (EPA recommends fixing your home)

### Bq/m³ (Becquerels per Cubic Meter)
- **Green**: < 100 Bq/m³
- **Orange**: 100 - 150 Bq/m³ (EPA recommends considering mitigation)
- **Red**: > 150 Bq/m³ (EPA recommends fixing your home)

## Known Limitations

- Requires EcoSense cloud account (no local/Bluetooth support)

## Troubleshooting

If you see a "Cannot connect" error, double-check your credentials and network.  
To enable debug logging, add the following to your `configuration.yaml`:

```yaml
logger:
  default: info
  logs:
    custom_components.ecosense_radon: debug
```

## Contributing

Pull requests are welcome! Please follow the code style enforced by `ruff`.
