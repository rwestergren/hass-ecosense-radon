# EcoSense Radon – Home Assistant Integration

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=rwestergren&repository=hass-ecosense-radon&category=integration)

[![HACS Custom](https://img.shields.io/badge/HACS-Custom-blue.svg?style=flat-square)](https://hacs.xyz/) [![GitHub issues](https://img.shields.io/github/issues/rwestergren/hass-ecosense-radon?style=flat-square)](https://github.com/rwestergren/hass-ecosense-radon/issues)

This custom integration connects EcoSense cloud-connected radon monitors to Home Assistant, providing current radon readings and alert levels.

## Features

- Radon Level sensor with configurable units (`pCi/L` or `Bq/m³`)
- Alert Level sensor (Green / Orange / Red) with EPA-based thresholds
- Device info and automatic cloud polling every 5 minutes
- Unit configuration during setup and changeable via integration options
- Bundled brand icon/logo (light and dark variants) shown in the UI

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

## What to do if your level is Orange or Red

Seeing an Orange or Red alert does not mean you need to panic — radon
levels fluctuate with weather, ventilation, and the season. What matters
most is your long-term average, so use the alert as a prompt to act,
not as a single definitive verdict.

**First, confirm the reading.**

- Check your long-term average in Home Assistant (weeks, not a single
  day). A short spike after a storm or a closed-up house is common.
- If the average stays Orange or Red, confirm it with a second test:
  a long-term test kit (90+ days) or a second continuous monitor placed
  in the same room, ideally the lowest lived-in level of the home.

**If your level is Orange (2.7–4.0 pCi/L / 100–150 Bq/m³):**

- Increase ventilation: open windows regularly when weather allows and
  make sure your home's existing ventilation is working as intended.
- Seal obvious entry points — cracks in the foundation and basement
  floor, gaps around pipes, and sump pits — to reduce radon entry.
- Keep monitoring and retest in 3–6 months. If the average is still
  Orange (or rising), start getting quotes for mitigation, especially
  if anyone in the household spends long hours in the lowest level.

**If your level is Red (> 4.0 pCi/L / > 150 Bq/m³):**

- The EPA recommends fixing your home. The standard solution is an
  active soil depressurization system (also called sub-slab
  depressurization): a fan and pipe system that draws radon from
  beneath the foundation and vents it safely outside.
- Hire a certified radon mitigation professional to design and install
  the system — sizing and sealing depend on your foundation type, so
  this is not a typical DIY job.
- After mitigation, keep the monitor running and retest to confirm the
  system brought your long-term average down into the Green range.

Further reading: [radon testing and mitigation costs](https://theradonlab.com/)

## Known Limitations

- Requires EcoSense cloud account (no local/Bluetooth support)
- The bundled integration icon/logo requires Home Assistant **2026.3** or newer,
  which added support for local brand images in custom integrations
  ([announcement](https://developers.home-assistant.io/blog/2026/02/24/brands-proxy-api)).
  On older versions, the images are ignored and Home Assistant falls back to the
  brands CDN (where this integration is not registered), so the generic
  placeholder is shown.

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

