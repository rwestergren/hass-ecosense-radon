"""Constants for the EcoSense Radon integration."""

DOMAIN = "ecosense_radon"

# Constants for EcoSense API
USER_POOL_ID = "us-west-2_vB73oNa7f"
CLIENT_ID = "1dk9ul54cdo42lt6e9u1oa9g1d"
USER_POOL_REGION = "us-west-2"
API_URL = "https://api.cloud.ecosense.io/api/v1/device"

# Configuration keys from Home Assistant
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Data update interval in minutes
UPDATE_INTERVAL = 5

# Radon unit types
UNIT_PCIL = 0
UNIT_BQM3 = 1

# Radon units
RADON_CONCENTRATION_BECQUERELS_PER_CUBIC_METER = "Bq/m³"
RADON_CONCENTRATION_PICOCURIES_PER_LITER = "pCi/L"
RADON_UNIT_CONVERSION_SCALE = 37.0

# EPA thresholds
EPA_CONSIDER_FIXING_HOME = 2.7  # pCi/L
EPA_RECOMMEND_FIXING_HOME = 4.0  # pCi/L
EPA_CONSIDER_FIXING_HOME_BQ = 100  # Bq/m³
EPA_RECOMMEND_FIXING_HOME_BQ = 150  # Bq/m³

# Configuration keys
CONF_UNIT = "unit"
