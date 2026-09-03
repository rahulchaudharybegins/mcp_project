import httpx


# ============================================================
# 1. WEATHER TOOL
# ============================================================

async def get_weather(
    latitude: float,
    longitude: float
) -> dict:
    """
    Get current weather from Open-Meteo.

    No API key required.
    """

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "precipitation,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# 2. CURRENCY TOOL
# ============================================================

async def get_exchange_rate(
    base_currency: str,
    quote_currency: str
) -> dict:
    """
    Get current exchange rate from Frankfurter.

    No API key required.
    """

    base_currency = base_currency.upper()
    quote_currency = quote_currency.upper()

    url = (
        "https://api.frankfurter.dev/v2/"
        f"rate/{base_currency}/{quote_currency}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            timeout=20
        )

        response.raise_for_status()

        return response.json()


# ============================================================
# 3. COUNTRY TOOL
# ============================================================

async def get_country(
    country_code: str
) -> dict:
    """
    Get country information from countries.dev.

    No API key required.
    """

    country_code = country_code.upper()

    url = (
        f"https://countries.dev/alpha/"
        f"{country_code}"
    )

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url,
            timeout=20
        )

        response.raise_for_status()

        return response.json()