from mcp.server.mcpserver import MCPServer

from server.tools import (
    get_weather,
    get_exchange_rate,
    get_country,
)


# ============================================================
# CREATE MCP SERVER
# ============================================================

mcp = MCPServer(
    "External API MCP Server"
)


# ============================================================
# TOOL 1 — WEATHER
# ============================================================

@mcp.tool()
async def weather(
    latitude: float,
    longitude: float
) -> dict:
    """
    Get current weather for a location.

    Uses the Open-Meteo API.
    No API key required.
    """

    return await get_weather(
        latitude=latitude,
        longitude=longitude
    )


# ============================================================
# TOOL 2 — EXCHANGE RATE
# ============================================================

@mcp.tool()
async def exchange_rate(
    base_currency: str,
    quote_currency: str
) -> dict:
    """
    Get the latest exchange rate between two currencies.

    Uses the Frankfurter API.
    No API key required.
    """

    return await get_exchange_rate(
        base_currency=base_currency,
        quote_currency=quote_currency
    )


# ============================================================
# TOOL 3 — COUNTRY
# ============================================================

@mcp.tool()
async def country(
    country_code: str
) -> dict:
    """
    Get country information.

    Uses the countries.dev API.
    No API key required.
    """

    return await get_country(
        country_code=country_code
    )


# ============================================================
# START MCP SERVER
# ============================================================

if __name__ == "__main__":

    mcp.run(
        "streamable-http",
        host="127.0.0.1",
        port=8000
    )