# How to connect ZenMaid to Claude Code, ChatGPT and any AI agent

**Yes, Claude, ChatGPT and other AI agents can work in your ZenMaid account.** ZenMaid has no official app in the ChatGPT or Claude directories, and its documentation points integrations to Zapier. Cotlet.dev connects your own signed-in ZenMaid account to any AI agent, so you can ask in plain words and the AI schedules jobs, finds openings and updates customers for you.

## What you can ask

> Schedule a 3-hour deep clean for Maria Lopez at 42 Oak Street on Thursday at 9 am with Team B.

> Where are the open slots next week for a 2-hour standard clean? List them by day.

> Add a new customer, David Chen at 18 Pine Ave, with a biweekly clean every other Monday at 1 pm.

> Which recurring customers have no job booked in the next 30 days? Show their last clean date.

> Move all of Kelly's Friday jobs to Rosa and list the customers affected.

## Connect in 2 minutes

Get your API key at https://cotlet.dev/app and export it as `COTLET_API_KEY`.

### Claude Code

```bash
claude mcp add --transport http cotlet https://cotlet.dev/mcp/v1 --header "Authorization: Bearer $COTLET_API_KEY"
```

### ChatGPT

Settings → Apps → add connector URL `https://cotlet.dev/mcp/v1`, then sign in with Cotlet.dev. No API key needed.

### Cursor

Copy `.cursor/mcp.json` from this repo into your project:

```json
{
  "mcpServers": {
    "cotlet": {
      "url": "https://cotlet.dev/mcp/v1",
      "headers": {
        "Authorization": "Bearer ${COTLET_API_KEY}"
      }
    }
  }
}
```

## Run it locally (stdio)

This repo is a real MCP server. It speaks MCP over stdio, lists its ZenMaid tools without any key, and forwards every tool call to the hosted Cotlet.dev server. The hosted URL above stays the recommended way. Use this when your client only starts local servers.

```json
{"mcpServers":{"zenmaid":{"command":"uvx","args":["zenmaid-mcp"],"env":{"COTLET_API_KEY":"your-key"}}}}
```

Or with Docker:

```bash
docker build -t zenmaid-mcp .
docker run -i --rm -e COTLET_API_KEY zenmaid-mcp
```

Tools: `zenmaid_guide`, `zenmaid_status`, `zenmaid_open`, `zenmaid_read`, `zenmaid_click`, `zenmaid_type`, `zenmaid_close`. Without `COTLET_API_KEY` a tool call answers: "Set COTLET_API_KEY. Get a key at https://cotlet.dev/app".

## Command line

Python 3.10+, nothing else to install. From PyPI:

```bash
pip install zenmaid-mcp        # or run it once: uvx zenmaid-mcp connect
zenmaid-mcp connect
```

Or straight from this repo:

```bash
export COTLET_API_KEY="your-key"
python3 zenmaid_agent.py connect   # ready config for Claude Code, Cursor, ChatGPT
python3 zenmaid_agent.py status    # is ZenMaid ready in your Cotlet.dev account
python3 zenmaid_agent.py guide     # ZenMaid screens and sign-in link
python3 zenmaid_agent.py read      # open ZenMaid, read the page, close the browser
python3 zenmaid_agent.py tools     # list Cotlet.dev tools
python3 zenmaid_agent.py serve     # start the stdio MCP server (same as no argument)
```

## Questions from ZenMaid users

**Does ZenMaid have an API?**

ZenMaid's documentation directs integrations through Zapier. Cotlet.dev works in your ZenMaid account directly, so your AI agent can schedule jobs and manage customers without setting up Zaps.

**How do I connect ZenMaid to ChatGPT?**

Add Cotlet.dev as an app in ChatGPT (Settings → Apps, connector URL `https://cotlet.dev/mcp/v1`), sign in to ZenMaid once in your Cotlet.dev Cloud Browser, and ask ChatGPT in plain words. No code and no ZenMaid API key.

**Is there a way to use Claude with ZenMaid?**

Yes. In Claude Code run the one-line `claude mcp add` command above; in the Claude app add `https://cotlet.dev/mcp/v1` as a custom connector. Claude then works in your own ZenMaid account.

**Is there a ZenMaid MCP server?**

ZenMaid has no official MCP server. Zapier offers a third-party ZenMaid MCP connection. Cotlet.dev is a hosted MCP server that works in ZenMaid for you, 24/7, with Claude, ChatGPT, Cursor, Codex, n8n, Make and Zapier.

## Find it on

- [ZenMaid on Cotlet.dev](https://cotlet.dev/integrations/zenmaid-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=zenmaid&utm_content=find)
- [PyPI package zenmaid-mcp](https://pypi.org/project/zenmaid-mcp/)
- [Odel](https://odel.app/modules/cotlet/zenmaid)
- [mcpbeat](https://mcpbeat.com/mcp-servers/cotlet/zenmaid/)
- [Step-by-step guide (PDF) on Internet Archive](https://archive.org/details/cotlet-connect-zenmaid-to-ai-agents-guide)

## Also works with

- [Mangomint MCP](https://github.com/cotlet-connect/mangomint-mcp)
- [Wanderlog MCP](https://github.com/cotlet-connect/wanderlog-mcp)
- [SmugMug MCP](https://github.com/cotlet-connect/smugmug-mcp)
- [Garmin Connect MCP](https://github.com/cotlet-connect/garmin-mcp)
- [Housecall Pro MCP](https://github.com/cotlet-connect/housecall-pro-mcp)
- [Medium MCP](https://github.com/cotlet-connect/medium-mcp)
- [Crexi MCP](https://github.com/cotlet-connect/crexi-mcp)
- [DistroKid MCP](https://github.com/cotlet-connect/distrokid-mcp)
- [LinkedIn MCP](https://github.com/cotlet-connect/linkedin-mcp)
- [EstimateOne MCP](https://github.com/cotlet-connect/estimateone-mcp)
- [Google Search Console MCP](https://github.com/cotlet-connect/google-search-console-mcp)
- [Lichess MCP](https://github.com/cotlet-connect/lichess-mcp)
- [Strava MCP](https://github.com/cotlet-connect/strava-mcp)
- [StreamElements MCP](https://github.com/cotlet-connect/streamelements-mcp)
- [Meetup MCP](https://github.com/cotlet-connect/meetup-mcp)
- [AccuRanker MCP](https://github.com/cotlet-connect/accuranker-mcp)
- [GetYourGuide MCP](https://github.com/cotlet-connect/getyourguide-mcp)
- [Idealista MCP](https://github.com/cotlet-connect/idealista-mcp)
- [Riverside MCP](https://github.com/cotlet-connect/riverside-mcp)
- [Udemy MCP](https://github.com/cotlet-connect/udemy-mcp)
- [Faire MCP](https://github.com/cotlet-connect/faire-mcp)
- [Teachable MCP](https://github.com/cotlet-connect/teachable-mcp)
- [Vagaro MCP](https://github.com/cotlet-connect/vagaro-mcp)
- [Buildertrend MCP](https://github.com/cotlet-connect/buildertrend-mcp)
- [Zoopla MCP](https://github.com/cotlet-connect/zoopla-mcp)
- [Dribbble MCP](https://github.com/cotlet-connect/dribbble-mcp)
- [Hostelworld MCP](https://github.com/cotlet-connect/hostelworld-mcp)
- [Mashvisor MCP](https://github.com/cotlet-connect/mashvisor-mcp)
- [Rent Manager MCP](https://github.com/cotlet-connect/rent-manager-mcp)
- [ThriveCart MCP](https://github.com/cotlet-connect/thrivecart-mcp)
- [Fresha MCP](https://github.com/cotlet-connect/fresha-mcp)
- [Booksy MCP](https://github.com/cotlet-connect/booksy-mcp)
- [BookingKoala MCP](https://github.com/cotlet-connect/bookingkoala-mcp)
- [Milanote MCP](https://github.com/cotlet-connect/milanote-mcp)
- [Partiful MCP](https://github.com/cotlet-connect/partiful-mcp)
- [Contractor Foreman MCP](https://github.com/cotlet-connect/contractor-foreman-mcp)
- [Pixieset MCP](https://github.com/cotlet-connect/pixieset-mcp)
- [GlossGenius MCP](https://github.com/cotlet-connect/glossgenius-mcp)
- [All apps connected through Cotlet.dev](https://github.com/cotlet-connect)

---

More: https://cotlet.dev/integrations/zenmaid-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=zenmaid

Start free: https://cotlet.dev/signup?app=zenmaid&utm_source=github&utm_medium=readme&utm_campaign=zenmaid
