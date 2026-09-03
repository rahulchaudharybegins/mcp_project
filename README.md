**`@mcp.tool()` is registering the function as an MCP tool.** It is **not calling the function at that moment**.

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



Exactly — **you've identified the key point**. A server cannot receive a request if it isn't running.

Your understanding should be:

> **The MCP server must already be running/listening before the client can call its tools.**

There are actually **two different things** happening, and this is where the confusion comes from.

### 1. You start the MCP server

When you run:

```powershell
python server.py
```

Python reaches:

```python
if __name__ == "__main__":
    mcp.run(
        "streamable-http",
        host="127.0.0.1",
        port=8000
    )
```

Now the MCP server starts.

Conceptually:

```text
server.py
   │
   ▼
MCPServer
   │
   ├── weather       ← registered
   ├── exchange_rate ← registered
   └── country       ← registered
   │
   ▼
HTTP server starts
127.0.0.1:8000
   │
   │  "I'm listening"
   ▼
WAITING FOR CLIENT
```

At this point, your server is **alive and waiting**.

---

### 2. Client connects/calls the server

Later, your MCP client sends a request:

```text
Client
   │
   │ HTTP request
   │ "Call weather"
   ▼
127.0.0.1:8000
   │
   ▼
MCP Server
   │
   ▼
weather(latitude, longitude)
   │
   ▼
get_weather()
```

So the server doesn't magically start when the client calls it.

**Something must start the server first.**

---

# But there is one important exception

This is where MCP gets interesting.

With **stdio transport**, the client can start the MCP server itself.

For example:

```text
MCP Client
    │
    │ starts
    ▼
python server.py
    │
    ▼
MCP Server process
    │
    │ stdin/stdout
    ▼
MCP Client
```

The client launches your server as a **child process**.

For example, conceptually:

```python
subprocess.Popen(
    ["python", "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE
)
```

So you might think:

> "I didn't manually start `server.py`, but the client was able to call it."

That's because **the client started it for you**.

---

# Your code is different

You are using:

```python
mcp.run(
    "streamable-http",
    host="127.0.0.1",
    port=8000
)
```

That's **Streamable HTTP**, not stdio.

Therefore, normally you have:

```text
Terminal 1
──────────

python server.py
       │
       ▼
MCP Server
127.0.0.1:8000
       │
       │ waiting
       ▼


Terminal 2
──────────

python client.py
       │
       │ HTTP request
       ▼
127.0.0.1:8000
       │
       ▼
MCP Server
       │
       ▼
weather()
```

If Terminal 1 isn't running:

```text
Client
  │
  │ HTTP request
  ▼
127.0.0.1:8000
  │
  X
Connection refused
```

There is nobody listening on port `8000`.

---

## This is the key mental model

Don't think:

```text
Client calls tool
       ↓
Server magically starts
       ↓
Function executes
```

Instead:

### HTTP MCP

```text
       START
         │
         ▼
   MCP Server process
         │
         ▼
   HTTP server listening
      :8000
         │
         │ waiting...
         │
         │
     Client connects
         │
         ▼
    MCP request
         │
         ▼
   Find registered tool
         │
         ▼
     weather()
         │
         ▼
   get_weather()
```

### stdio MCP

```text
Client
   │
   │ starts process
   ▼
MCP Server process
   │
   ▼
register tools
   │
   ▼
wait for messages
   │
   │ stdin
   ▼
MCP request
   │
   ▼
weather()
```

So your statement:

> "In general, when client calls, server invokes."

is **almost right**, but I'd refine it to:

> **The server must be running first. The client sends a tool-call request to the running MCP server, and the MCP server then invokes the registered function.**

And with **stdio**, the client may be responsible for **starting the server process first**.

That distinction between **server lifecycle** and **tool invocation** is fundamental to understanding MCP.

