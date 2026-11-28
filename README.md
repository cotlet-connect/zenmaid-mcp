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

## What you can ask your AI to do in ZenMaid

These are real jobs ZenMaid users asked about. Cotlet lets ChatGPT, Claude or any MCP client do them in your own signed-in ZenMaid account.

### Exports and your data

#### How do I export all my ZenMaid customers, appointments and payroll to CSV when my plan does not include exports?

Yes. ZenMaid's own Data exports are on the Pro Max plan only. With Cotlet, ChatGPT or Claude opens your signed-in ZenMaid account, reads the Contacts, Scheduling and Payroll pages and gives you the rows as a CSV or a Google Sheet.

Ask your agent: "Read all my ZenMaid contacts and this month's appointments and give me one CSV with name, address, service, date and price."

As an API endpoint: Yes. Do the export once with your agent in Cotlet and save it as an endpoint, then call it every morning from n8n, Make or Zapier to add the day's appointments to Google Sheets.

#### How do I get all my records out of ZenMaid before I cancel?

Yes. With Cotlet, your agent goes through your signed-in ZenMaid account page by page: contacts, recurring services, past appointments, invoices and cleaners. It saves each list as a file you keep, so you can cancel without losing your history.

Ask your agent: "Save every ZenMaid contact, recurring service, past appointment and invoice to separate CSV files before I cancel my plan."

#### How do I import my customers and recurring schedule into ZenMaid from Jobber or a spreadsheet?

Partly. ZenMaid has no self-serve import; its team imports a file for you in 2 to 4 business days. With Cotlet, your agent can add the customers and recurring services one by one in ZenMaid from your spreadsheet. Nothing is created until you say yes.

Ask your agent: "Take the customers in this spreadsheet and add each one to ZenMaid with their address and recurring service. Show me the first five before you start."

### Invoices, QuickBooks and profit

#### How do I connect ZenMaid to QuickBooks Online so invoices and customers sync without retyping?

Yes. ZenMaid's help centre offers QuickBooks only through Zapier on Pro Max. With Cotlet, your agent reads the day's completed jobs in ZenMaid and enters the matching invoices in QuickBooks Online, both signed in in your Cloud Browser. Nothing is entered until you say yes.

Ask your agent: "Take today's completed ZenMaid jobs and create the matching invoices in QuickBooks Online. Show me the list before you enter anything."

As an API endpoint: Yes. Save the daily invoice run as an endpoint in Cotlet and call it every evening from n8n, Make or Zapier.

#### How do I automate invoices and late-payment reminders in ZenMaid?

Yes. With Cotlet, ChatGPT or Claude lists the unpaid invoices in your ZenMaid account, sorts them by how late they are and drafts a polite reminder for each client. Nothing is sent until you say yes.

Ask your agent: "List my unpaid ZenMaid invoices older than 7 days and draft a short reminder for each client."

As an API endpoint: Yes. Save the unpaid invoice list as an endpoint in Cotlet and call it every Monday from n8n, Make or Zapier.

#### Can AI tell me profit per hour per job type from my ZenMaid data?

Yes. With Cotlet, your agent reads revenue per appointment and the clocked hours report in ZenMaid, then works out revenue and labour cost per hour for each service type. ZenMaid's metric view leaves out tips and taxes, so the agent says which numbers it used.

Ask your agent: "From last month's ZenMaid appointments and clocked hours, show revenue and labour cost per hour for each service type."

As an API endpoint: Yes. Save the monthly profit table as an endpoint in Cotlet and call it from n8n, Make or a script on the first of each month.

### Payroll and hours

#### Can AI check my cleaners' hours in ZenMaid, fix forgotten clock-outs and warn me before payroll?

Yes. With Cotlet, ChatGPT or Claude reads the clocked hours report in your ZenMaid account, lists shifts with no clock-out or odd lengths and proposes the right end time for each. Nothing changes until you say yes.

Ask your agent: "Check this week's ZenMaid clocked hours, list shifts with no clock-out or over 10 hours, and propose the right end time for each."

As an API endpoint: Yes. Save the check as an endpoint in Cotlet and call it from n8n, Make or Zapier every Friday before you run payroll.

#### How do I send ZenMaid payroll to Gusto, ADP or Paychex without retyping hours?

Yes. With Cotlet, your agent reads each cleaner's hours and pay in ZenMaid's Payroll page and enters them in Gusto, ADP or Paychex, signed in in the same Cloud Browser. Nothing is submitted until you say yes.

Ask your agent: "Take this pay period's hours from ZenMaid Payroll and fill them into Gusto for each cleaner. Stop before submitting."

As an API endpoint: Yes. Save the payroll read as an endpoint in Cotlet that returns hours per cleaner as JSON, and pass it to your payroll tool from n8n or Make.

### Leads, quotes and win-backs

#### Can AI write and send follow-ups to the quotes I sent from ZenMaid and stop when the client replies?

Yes. With Cotlet, ChatGPT or Claude lists the ZenMaid leads with a quote and no booking, drafts a follow-up for each and skips anyone who already replied. Nothing is sent until you say yes.

Ask your agent: "List ZenMaid leads quoted in the last 14 days with no booking and draft a follow-up for each one who has not replied."

As an API endpoint: Yes. Save the open-quote list as an endpoint in Cotlet and call it every two days from n8n, Make or Zapier.

#### Can AI tell me which ZenMaid clients stopped rebooking and write a win-back message?

Yes. With Cotlet, your agent finds clients in ZenMaid whose last clean was more than 60 days ago and who have no future appointment, then writes a short win-back message for each. Nothing is sent until you say yes.

Ask your agent: "Find ZenMaid clients with no clean in 60 days and nothing booked, and draft a win-back message for each."

As an API endpoint: Yes. Save the lapsed-client list as an endpoint in Cotlet and call it monthly from n8n, Make or Zapier.

#### How do I connect ZenMaid to GoHighLevel so new contacts and leads follow up automatically?

Yes. With Cotlet, your agent reads new ZenMaid contacts and leads and adds them to GoHighLevel, both signed in in your Cloud Browser, so your GoHighLevel follow-ups start. Nothing is added until you say yes.

Ask your agent: "Add every ZenMaid lead from the last 7 days to GoHighLevel as a contact with their phone, email and the service they asked about."

As an API endpoint: Yes. Save the new-lead read as an endpoint in Cotlet and call it hourly from n8n or Make to push leads into GoHighLevel.

#### How do I get leads from my website, Facebook or property-manager emails into ZenMaid automatically?

Yes. With Cotlet, ChatGPT or Claude reads the lead from your inbox or Facebook page and adds it as a lead contact in ZenMaid with the details it found. Nothing is created until you say yes.

Ask your agent: "Read today's new lead emails and add each person to ZenMaid as a lead with name, phone, address and the service they want."

### Reminders and reviews

#### How do I get ZenMaid, Zapier and Quo (OpenPhone) to send appointment reminders?

Partly. ZenMaid can send up to two text and two email reminders per appointment on its own. With Cotlet, your agent lists tomorrow's ZenMaid appointments and drafts each reminder for Quo or your own phone line. Cotlet does not send texts itself, and nothing goes out until you say yes.

Ask your agent: "List tomorrow's ZenMaid appointments with client phone and time, and write a reminder text for each that I can send from Quo."

As an API endpoint: Yes. Save tomorrow's appointment list as an endpoint in Cotlet and call it every afternoon from n8n, Make or Zapier to send the texts through Quo.

#### How do I automate Google review requests after each ZenMaid clean?

Partly. ZenMaid's service rating can invite happy clients to Google and Yelp on its own. With Cotlet, your agent lists the cleans finished today without a rating and drafts a review request for each. Nothing is sent until you say yes.

Ask your agent: "List today's finished ZenMaid cleans with no service rating and draft a short Google review request for each client."

As an API endpoint: Yes. Save the list of today's finished cleans as an endpoint in Cotlet and call it every evening from n8n, Make or Zapier.

### Schedule and routes

#### Can Claude or ChatGPT check ZenMaid for first-time cleans and flag odd job notes before they cause a problem?

Yes. With Cotlet, ChatGPT or Claude reads tomorrow's schedule in your ZenMaid account, marks first-time clients and lists notes that need a call, such as pets, keys or access codes.

Ask your agent: "Check tomorrow's ZenMaid schedule, list first-time clients and any job notes about keys, pets, access or special requests."

As an API endpoint: Yes. Save the check as an endpoint in Cotlet and call it every evening from n8n, Make or Zapier to get the list by email.

#### Can AI plan the daily routes for my teams from ZenMaid appointments?

Partly. ZenMaid's Daily Route map shows the day's stops with no optimisation. With Cotlet, your agent reads each team's appointments and addresses and proposes an order of stops with drive times. Moving appointments in ZenMaid waits until you say yes.

Ask your agent: "Read tomorrow's ZenMaid appointments per team and propose the shortest order of stops for each team with estimated drive times."

#### How do I change or cancel many recurring cleans at once in ZenMaid without opening each one?

Yes. With Cotlet, your agent opens each recurring service in ZenMaid for you and makes the same change, such as a new price, a new day or a stop date. Nothing changes until you say yes to the list.

Ask your agent: "Find every ZenMaid recurring service for the Oak Street building and set it to stop after December 31. Show me the list first."

#### How do I sync ZenMaid with Google Calendar so my clients can see their next recurring cleans?

Partly. ZenMaid has no two-way calendar sync. With Cotlet, your agent reads upcoming cleans in ZenMaid and adds or updates the events in your Google Calendar, signed in in the same Cloud Browser. Nothing is added until you say yes.

Ask your agent: "Add next month's ZenMaid cleans to my Google Calendar, one event per appointment with client name and address."

As an API endpoint: Yes. Save the upcoming-cleans read as an endpoint in Cotlet and call it daily from n8n or Make to update Google Calendar.

### Safety

#### Is it safe to let an AI agent log in to my ZenMaid account and run tasks on a schedule?

Yes. With Cotlet, the agent works in your own signed-in ZenMaid session in a Cloud Browser, never sees your password and asks before it changes or sends anything. You can turn ZenMaid off for agents or delete the key at any time.

Ask your agent: "Before you change anything in ZenMaid, show me what you plan to do and wait for my OK."

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
