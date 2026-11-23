# ZenMaid API integration and MCP server: connect ZenMaid to ChatGPT, Claude and any AI agent

ZenMaid API integration and MCP server, unofficial, by Cotlet. Your AI works in your own signed-in ZenMaid account: the schedule, recurring cleans, cleaners, clock-ins and payroll, customers, estimates and invoices, on the same screens your login opens. No developer and no ZenMaid API key needed. Cotlet is independent and is not affiliated with ZenMaid.

**Does ZenMaid have an API or an MCP server?** ZenMaid has no public API: its help center says it has "no REST endpoints, webhook subscriptions, or programmatic data access", only Zapier (checked 23 Nov 2026). Its Zapier app, on the Pro Max plan, has 11 triggers and 4 create-only actions (appointment, booking, cleaner, customer); CSV exports are Pro Max only too. ZenMaid has no MCP server and no ChatGPT or Claude app; its own magazine suggests letting Claude or ChatGPT work in ZenMaid through a browser, which is what Cotlet does.

## What cleaning business owners ask their AI to do in ZenMaid

| Job | Ask your AI | Make it repeat |
|---|---|---|
| Payroll check | "Check this week's cleaner hours, find forgotten clock-outs and split overtime, before I run payroll." | Weekly |
| Hours for Gusto or ADP | "Total last week's hours and overtime per cleaner in the format I import into Gusto." | Weekly |
| Tomorrow's first-time cleans | "List tomorrow's first-time cleans and flag job notes that look unclear or risky." | Daily |
| Invoices from finished jobs | "Make invoices for today's completed jobs and list them for QuickBooks. Show me before you send any." | Daily |
| Clients who stopped rebooking | "List clients who have not had a clean in 6 weeks and draft a win-back message for each. Send nothing yet." | Weekly |
| Quote follow-ups | "List estimates sent this week with no answer and draft a follow-up for each." | Weekly |
| Profit per job type | "Show revenue, cleaner hours and profit per hour by job type for last month." | Monthly |
| Change many recurring cleans | "Move every Friday clean for the Rivera team next week to Thursday. Show me first." | When plans change |
| Leads into ZenMaid | "Add the leads from my website form and property-manager emails as customers with the requested clean." | Your own endpoint, called from your form tool or GoHighLevel |
| Appointments in a spreadsheet | "Put each day's appointments with team, customer and price in my Google Sheet." | Your own endpoint, called from Google Sheets |
| Records out before you cancel | "Export all customers, appointments and payroll before I cancel, even on a plan without CSV export." | Once |

Your AI asks you before it sends, books or changes anything. Payments stay in your hands: Cotlet refuses payments.

## Your own ZenMaid API, built with Cotlet

ZenMaid gives you no API; its Zapier app only creates records, on the Pro Max plan. With Cotlet you build your own: your AI does the job once in your Cloud Browser, you save it as an endpoint, and you call it from Google Sheets, QuickBooks, Gusto, GoHighLevel, Zapier, Make, n8n, your own code.

Examples you can build in a few minutes (none of them exists until you build it):

| Endpoint you build | What it returns or does |
|---|---|
| `appointments-for-day` | appointments for a date with team, customer, address and price |
| `cleaner-hours` | clock-ins, hours and overtime per cleaner for a period |
| `completed-jobs` | jobs completed on a date, ready to invoice |
| `lapsed-customers` | customers with no clean for the weeks you name |
| `open-estimates` | estimates with no answer, with customer and total |
| `new-customer` | adds a customer with address and the requested clean (writes only after you allow it) |

Call it with your Cotlet API key, JSON in and JSON out:

```bash
curl -X POST https://cotlet.dev/api/v1/custom/appointments-for-day \
  -H "Authorization: Bearer $COTLET_API_KEY" -H "Content-Type: application/json" -d '{}'
```

Limits: one call runs up to 90 seconds, writes wait for your consent, payments are blocked. Start here: https://cotlet.dev/app/custom-api/new?app=zenmaid

## Connect in 2 minutes

Sign up at https://cotlet.dev, sign in to ZenMaid once in your Cloud Browser, then add Cotlet to your AI.

### Claude

Settings → Connectors → Add custom connector, paste `https://cotlet.dev/mcp/v1` and sign in with Cotlet.dev.

### ChatGPT

Open Plugins in ChatGPT, choose Create as a plugin, paste `https://cotlet.dev/mcp/v1` and sign in with Cotlet.dev. No API key needed.

### Claude Code

```bash
claude mcp add --transport http cotlet https://cotlet.dev/mcp/v1 --header "Authorization: Bearer $COTLET_API_KEY"
```

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

## Questions from ZenMaid owners
**Does ZenMaid have an API?**

No. ZenMaid's help center says it has no REST endpoints, webhook subscriptions or programmatic data access, only Zapier (checked 23 Nov 2026). With Cotlet you build your own endpoints in your signed-in ZenMaid account.

**Is there an official ZenMaid MCP server or ChatGPT app?**

No. ZenMaid's own magazine suggests letting Claude or ChatGPT work in ZenMaid through a browser. Cotlet does that in your own Cloud Browser and works in the ChatGPT and Claude apps and any MCP client.

**How do I send ZenMaid hours to Gusto, ADP or Paychex?**

Your AI totals hours and overtime per cleaner, fixes forgotten clock-outs after your OK and prepares the file your payroll tool imports.

**How do I get ZenMaid invoices into QuickBooks?**

Your AI makes invoices for completed jobs and lists them, with customers, for your QuickBooks import or bookkeeper.

**Can AI follow up on my ZenMaid estimates?**

Yes. It lists estimates with no answer and drafts a follow-up for each. Nothing goes out until you say yes.

**How do I export my ZenMaid data without the Pro Max plan?**

CSV export is a Pro Max feature. Your AI reads customers, appointments and payroll from the screens your login opens and saves them to a spreadsheet.

**Is it safe to let an AI agent work in my ZenMaid account?**

Cotlet works in your own signed-in session in your Cloud Browser and asks you before it sends, books or changes anything.

## Find it on

- [ZenMaid MCP server on Cotlet.dev](https://cotlet.dev/integrations/zenmaid-api-mcp-server?utm_source=github&utm_medium=readme&utm_campaign=zenmaid&utm_content=find)
- [ZenMaid API with Cotlet](https://cotlet.dev/integrations/api/zenmaid?utm_source=github&utm_medium=readme&utm_campaign=zenmaid&utm_content=find)
- [Does ZenMaid have an API or MCP server?](https://cotlet.dev/api-mcp-status/zenmaid?utm_source=github&utm_medium=readme&utm_campaign=zenmaid&utm_content=find)
- [PyPI package zenmaid-mcp](https://pypi.org/project/zenmaid-mcp/)

## More cleaning apps on Cotlet

- [BookingKoala MCP](https://github.com/cotlet-connect/bookingkoala-mcp)
- [Housecall Pro MCP](https://github.com/cotlet-connect/housecall-pro-mcp)
- [Service Autopilot MCP](https://github.com/cotlet-connect/service-autopilot-mcp)
- [Invoice Simple MCP](https://github.com/cotlet-connect/invoice-simple-mcp)
