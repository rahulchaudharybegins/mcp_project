Yes — **`@mcp.tool()` is registering the function as an MCP tool.** It is **not calling the function at that moment**.

The important distinction is:

```python
@mcp.tool()
async def weather(latitude: float, longitude: float) -> dict:
    return await get_weather(
        latitude=latitude,
        longitude=longitude
    )
```

Think of it as a **registration process**.

### What happens step by step

When Python loads your `server.py`, it encounters:

```python
@mcp.tool()
async def weather(...):
    ...
```

Python essentially does something conceptually like:

```python
weather = mcp.tool()(weather)
```

The MCP server then records something like:

```text
MCP Server
│
├── weather
│   ├── description: "Get current weather..."
│   ├── input: latitude, longitude
│   └── function: weather()
│
├── exchange_rate
│   ├── input: base_currency, quote_currency
│   └── function: exchange_rate()
│
└── country
    ├── input: country_code
    └── function: country()
```

So **nothing is calling `get_weather()` yet**.

---

## When is `weather()` actually called?

It happens later when an MCP client/AI agent sends a tool-call request to your server.

For example, conceptually:

```text
MCP Client
    │
    │ "Call weather with latitude=17.38,
    │  longitude=78.48"
    ▼
MCP Server
    │
    │ finds registered "weather" tool
    ▼
weather(
    latitude=17.38,
    longitude=78.48
)
    │
    ▼
get_weather(...)
    │
    ▼
Open-Meteo API
```

So there are **two separate events**:

### 1. Server startup → registration

When this executes:

```python
mcp = MCPServer("External API MCP Server")
```

and then Python processes:

```python
@mcp.tool()
async def weather(...):
```

the function is **registered** with the MCP server.

Same for:

```python
@mcp.tool()
async def exchange_rate(...):
```

and:

```python
@mcp.tool()
async def country(...):
```

---

### 2. MCP client request → execution

Later, when the client says:

```text
Call the "weather" tool
with:
latitude = 17.38
longitude = 78.48
```

then:

```python
async def weather(
    latitude: float,
    longitude: float
) -> dict:
```

actually executes.

And **inside that function**:

```python
return await get_weather(
    latitude=latitude,
    longitude=longitude
)
```

is when your `get_weather()` function is called.

---

## A useful analogy

Think about a restaurant.

```python
@mcp.tool()
async def weather(...):
```

is like telling the restaurant:

> "Add `weather` to the menu."

You're **not cooking the dish yet**.

The MCP client later orders:

> "I want `weather(latitude=17.38, longitude=78.48)`."

Only then does the kitchen execute the function.

```text
@mcp.tool()
       │
       ▼
Register function
       │
       │
       │     MCP Client
       │         │
       │         │ tool call
       │         ▼
       └────► Execute function
                  │
                  ▼
             get_weather()
                  │
                  ▼
             External API
```

### One subtle but important point

Your `weather()` function is actually a **wrapper** around `get_weather()`:

```python
@mcp.tool()
async def weather(...):
    return await get_weather(...)
```

The MCP server exposes **`weather`** as the tool.

`get_weather` itself is **not automatically an MCP tool** just because it exists in `server.tools`.

So:

```text
MCP-visible tool
        ↓
     weather()
        ↓
   get_weather()
        ↓
 Open-Meteo API
```

That's a very common MCP architecture: **MCP tool → application/service function → external API**.
