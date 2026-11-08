#!/usr/bin/env python3
"""ZenMaid through Cotlet.dev: stdio MCP server and small CLI over the hosted Cotlet.dev MCP server (stdlib only)."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

START_URL = "https://zenmaid.com"
SLUG = "zenmaid"
URL = "https://cotlet.dev/mcp/v1"
GUIDE_FIELD = "app"
KEY_HELP = "Set COTLET_API_KEY. Get a key at https://cotlet.dev/app"
NAME = "ZenMaid"
JOB = "schedule cleaning jobs and manage customers"
VERSION = "1.1.0"
PREFIX = "zenmaid"
PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

CONFIG = {"mcpServers": {"cotlet": {"url": URL, "headers": {"Authorization": "Bearer ${COTLET_API_KEY}"}}}}


class Client:
    def __init__(self, key):
        self.key = key
        self.session = None
        self.next_id = 0

    def _post(self, payload):
        headers = {
            "Authorization": "Bearer " + self.key,
            "Accept": "application/json, text/event-stream",
            "Content-Type": "application/json",
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        req = urllib.request.Request(URL, json.dumps(payload).encode(), headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                self.session = resp.headers.get("Mcp-Session-Id") or self.session
                return resp.read().decode(), resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            raise RuntimeError("HTTP %s: %s" % (e.code, e.read().decode(errors="replace")[:300]))

    @staticmethod
    def _parse(body, ctype, rid):
        if "text/event-stream" in ctype:
            for line in body.splitlines():
                if line.startswith("data:"):
                    try:
                        msg = json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if msg.get("id") == rid:
                        return msg
            raise RuntimeError("No JSON-RPC answer in stream")
        return json.loads(body)

    def rpc(self, method, params=None):
        self.next_id += 1
        rid = self.next_id
        body, ctype = self._post({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}})
        msg = self._parse(body, ctype, rid)
        if "error" in msg:
            raise RuntimeError(msg["error"].get("message", str(msg["error"])))
        return msg.get("result", {})

    def start(self):
        self.rpc("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": SLUG + "-mcp", "version": "1.0.0"},
        })
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"})

    def call(self, tool, args):
        res = self.rpc("tools/call", {"name": tool, "arguments": args})
        text = "\n".join(c.get("text", "") for c in res.get("content", []) if c.get("type") == "text")
        if res.get("isError"):
            raise RuntimeError(text or "tool error")
        return text


def _obj(props, required=()):
    schema = {"type": "object", "properties": props, "additionalProperties": False}
    if required:
        schema["required"] = list(required)
    return schema


# Static tool list: answers tools/list without any key. Each tool forwards to one Cotlet.dev tool.
TOOLS = [
    (PREFIX + "_guide", "How to work in %s (%s): its screens and the sign-in link. Call this first." % (NAME, JOB),
     _obj({"task": {"type": "string", "description": "What you want done in %s, in your words." % NAME}})),
    (PREFIX + "_status", "Check that your Cotlet.dev account and %s are ready: account, credits and %s connection." % (NAME, NAME),
     _obj({})),
    (PREFIX + "_open", "Open a %s page in your signed-in Cloud Browser (default %s) to work with %s." % (NAME, START_URL, JOB),
     _obj({"url": {"type": "string", "description": "Page to open. Default: " + START_URL}})),
    (PREFIX + "_read", "Read the current %s page: its text and numbered buttons, links and fields." % NAME,
     _obj({"element": {"type": "integer", "minimum": 1, "description": "Read only inside this element."}})),
    (PREFIX + "_click", "Click a numbered element on the current %s page." % NAME,
     _obj({"element": {"type": "integer", "minimum": 1, "description": "Element number from the last read."}}, ["element"])),
    (PREFIX + "_type", "Type text into a numbered field on the current %s page." % NAME,
     _obj({"element": {"type": "integer", "minimum": 1, "description": "Field number from the last read."},
           "text": {"type": "string", "description": "Text to type."}}, ["element", "text"])),
    (PREFIX + "_close", "Close the %s browser session when the work is done, so credits stop running." % NAME,
     _obj({})),
]


def _forward(client, short, args):
    """Run one static tool against the hosted server; returns text."""
    if short == "guide":
        up = {GUIDE_FIELD: SLUG}
        if args.get("task"):
            up["task"] = str(args["task"])
        return client.call("cotlet_app_guide", up)
    if short == "status":
        return client.call("cotlet_whoami", {}) + "\n\n" + client.call("cotlet_apps", {"app": SLUG})
    if short == "open":
        return client.call("cotlet_browser_open", {"url": args.get("url") or START_URL})
    if short == "read":
        return client.call("cotlet_browser_read", {k: args[k] for k in ("element",) if k in args})
    if short == "click":
        return client.call("cotlet_browser_click", {"element": args["element"]})
    if short == "type":
        return client.call("cotlet_browser_type", {"element": args["element"], "text": args["text"]})
    return client.call("cotlet_browser_close", {})


class Server:
    def __init__(self):
        self.client = None

    def call_tool(self, name, args):
        short = name[len(PREFIX) + 1:] if name.startswith(PREFIX + "_") else ""
        if short not in [t[0][len(PREFIX) + 1:] for t in TOOLS]:
            return {"content": [{"type": "text", "text": "Unknown tool: %s" % name}], "isError": True}
        key = os.environ.get("COTLET_API_KEY")
        if not key:
            return {"content": [{"type": "text", "text": KEY_HELP}], "isError": True}
        try:
            if self.client is None:
                self.client = Client(key)
                self.client.start()
            text = _forward(self.client, short, args or {})
            return {"content": [{"type": "text", "text": text}]}
        except Exception as e:
            self.client = None
            return {"content": [{"type": "text", "text": str(e)}], "isError": True}

    def handle(self, msg):
        method, rid, params = msg.get("method"), msg.get("id"), msg.get("params") or {}
        if rid is None:
            return None  # notification
        if method == "initialize":
            want = params.get("protocolVersion")
            result = {
                "protocolVersion": want if want in PROTOCOLS else PROTOCOLS[0],
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SLUG + "-mcp", "version": VERSION},
                "instructions": "%s through Cotlet.dev. Call %s_guide first. Set COTLET_API_KEY (https://cotlet.dev/app)." % (NAME, PREFIX),
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": [{"name": n, "description": d, "inputSchema": s} for n, d, s in TOOLS]}
        elif method == "tools/call":
            result = self.call_tool(params.get("name", ""), params.get("arguments"))
        else:
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found: %s" % method}}
        return {"jsonrpc": "2.0", "id": rid, "result": result}


def serve():
    """MCP stdio transport: one JSON-RPC message per line on stdin/stdout, logs on stderr."""
    server = Server()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            reply = server.handle(msg) if isinstance(msg, dict) else None
        except ValueError:
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "Parse error"}}
        except Exception as e:
            print("Error: %s" % e, file=sys.stderr)
            reply = {"jsonrpc": "2.0", "id": msg.get("id"), "error": {"code": -32603, "message": str(e)}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply) + "\n")
            sys.stdout.flush()


def connect():
    print("Claude Code:\n  claude mcp add --transport http cotlet %s --header \"Authorization: Bearer $COTLET_API_KEY\"\n" % URL)
    print("Cursor (.cursor/mcp.json):\n" + json.dumps(CONFIG, indent=2) + "\n")
    print("ChatGPT:\n  Settings -> Apps -> add connector URL %s, sign in with Cotlet.dev (no API key)." % URL)


def main():
    p = argparse.ArgumentParser(description="ZenMaid through Cotlet.dev")
    sub = p.add_subparsers(dest="cmd")
    for name in ("serve", "connect", "status", "guide", "tools"):
        sub.add_parser(name)
    r = sub.add_parser("read")
    r.add_argument("url", nargs="?")
    args = p.parse_args()
    if args.cmd in (None, "serve"):
        return serve()
    if args.cmd == "connect":
        return connect()
    key = os.environ.get("COTLET_API_KEY")
    if not key:
        print(KEY_HELP)
        sys.exit(2)
    try:
        c = Client(key)
        c.start()
        if args.cmd == "tools":
            print("\n".join(t["name"] for t in c.rpc("tools/list").get("tools", [])))
        elif args.cmd == "status":
            print(c.call("cotlet_apps", {"app": SLUG}))
        elif args.cmd == "guide":
            print(c.call("cotlet_app_guide", {GUIDE_FIELD: SLUG}))
        elif args.cmd == "read":
            # Works in the user's Web browser, where they sign in to the app once.
            c.call("cotlet_browser_open", {"url": args.url or START_URL})
            try:
                print(c.call("cotlet_browser_read", {}))
            finally:
                c.call("cotlet_browser_close", {})
    except Exception as e:
        print("Error: %s" % e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
