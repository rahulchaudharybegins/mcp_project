import asyncio

from mcp import Client


SERVER_URL = "http://127.0.0.1:8000/mcp"


async def main():

    print("=" * 70)
    print("MCP CLIENT")
    print("=" * 70)

    print()
    print("Connecting to:")
    print(SERVER_URL)

    # ========================================================
    # CONNECT TO MCP SERVER
    # ========================================================

    async with Client(SERVER_URL) as client:

        print()
        print("Connected!")

        # ====================================================
        # SERVER INFORMATION
        # ====================================================

        print()
        print("=" * 70)
        print("SERVER INFORMATION")
        print("=" * 70)

        print()
        print("Server:")
        print(client.server_info)

        print()
        print("Protocol:")
        print(client.protocol_version)

        print()
        print("Capabilities:")
        print(client.server_capabilities)

        # ====================================================
        # DISCOVER TOOLS
        # ====================================================

        print()
        print("=" * 70)
        print("MCP TOOL DISCOVERY")
        print("=" * 70)

        tools_result = await client.list_tools()

        print()
        print(
            f"Number of tools: "
            f"{len(tools_result.tools)}"
        )

        for tool in tools_result.tools:

            print()
            print("-" * 70)

            print("NAME:")
            print(tool.name)

            print()
            print("DESCRIPTION:")
            print(tool.description)

            print()
            print("INPUT SCHEMA:")
            print(tool.input_schema)

        # ====================================================
        # WEATHER
        # ====================================================

        print()
        print("=" * 70)
        print("CALLING WEATHER TOOL")
        print("=" * 70)

        weather_result = await client.call_tool(
            "weather",
            {
                "latitude": 13.0827,
                "longitude": 80.2707
            }
        )

        print()
        print("Weather Result:")
        print(weather_result)

        # ====================================================
        # CURRENCY
        # ====================================================

        print()
        print("=" * 70)
        print("CALLING EXCHANGE RATE TOOL")
        print("=" * 70)

        currency_result = await client.call_tool(
            "exchange_rate",
            {
                "base_currency": "USD",
                "quote_currency": "INR"
            }
        )

        print()
        print("Exchange Rate Result:")
        print(currency_result)

        # ====================================================
        # COUNTRY
        # ====================================================

        print()
        print("=" * 70)
        print("CALLING COUNTRY TOOL")
        print("=" * 70)

        country_result = await client.call_tool(
            "country",
            {
                "country_code": "IN"
            }
        )

        print()
        print("Country Result:")
        print(country_result)

    # ========================================================
    # CONNECTION CLOSED
    # ========================================================

    print()
    print("=" * 70)
    print("MCP CLIENT FINISHED")
    print("=" * 70)


if __name__ == "__main__":

    asyncio.run(main())