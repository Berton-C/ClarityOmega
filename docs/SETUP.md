# ClarityOmega: Installation, Configuration, and Running

**Applies to:** ClarityOmega v0.1.0

This guide gets a new user from a clone to a running agent. For what the
system *is* and why it is built this way, read the README first. For what can
go wrong and what the agent is permitted to do, read
[`LIMITATIONS.md`](LIMITATIONS.md) before you start it.

> **Before you begin.** ClarityOmega runs continuously and acts without
> per-action approval: it executes shell commands, modifies files, searches the
> web, and sends messages on its own. Run it in an isolated environment. Do not
> point it at a machine holding credentials or data you care about.

---

## 1. Requirements

- **Docker** and **Docker Compose** (the reference deployment is Docker
  Compose on a single machine; it is developed on macOS, Apple silicon).
- **An API key** for at least one LLM provider: Anthropic, Friendli, or
  OpenAI. The reference deployment routes through a LiteLLM proxy.
- **Disk space.** The agent accumulates memory in ChromaDB and under
  `volumes/`. Budget a few gigabytes for sustained running.

You do **not** need a local MeTTa or SWI-Prolog installation. The PeTTa
runtime is built inside the container.

---

## 2. Clone

```bash
git clone https://github.com/Berton-C/ClarityOmega.git
cd ClarityOmega
```

All commands below run from the repository root.

---

## 3. Configure

Copy the example environment file and fill in real values:

```bash
cp .env.example .env
```

Open `.env` and set the following. `.env` is git-ignored and must never be
committed.

| Variable | Required | What it is |
|---|---|---|
| `ANTHROPIC_API_KEY` | one provider key required | Anthropic (Claude) API key |
| `FRIENDLI_API_KEY` | one provider key required | Friendli serverless API key |
| `OPENAI_API_KEY` | optional | OpenAI key; also used by the upstream memory system's embedding model. Commented out in `docker-compose.yml` by default; uncomment there too if you use it. |
| `MM_BOT_TOKEN` | yes | Mattermost bot personal access token |
| `MM_CHANNEL_ID` | yes | ID of the channel Clarity joins |
| `POSTGRES_PASSWORD` | strongly recommended | Password for the bundled PostgreSQL. Defaults to `mmuser_password` if unset, which is acceptable only for a strictly local deployment with no exposed ports. |

### Getting the Mattermost values

The Compose stack brings up its own Mattermost server. After first start
(section 4), reach it at `http://localhost:8065` and:

1. Create the first user; this account becomes the system administrator.
2. Create a team and the channel Clarity should speak in.
3. In the System Console, enable bot account creation, then create a bot
   account for Clarity.
4. Generate a personal access token for that bot. This is `MM_BOT_TOKEN`.
   It is shown once; copy it immediately.
5. Add the bot to your channel.
6. Get the channel ID: open the channel, then View Info. The channel ID is the
   long alphanumeric string, **not** the readable channel name.
7. Put both values in `.env` and restart the stack.

---

## 4. Build and run

```bash
docker compose build --no-cache && docker compose up -d
```

`--no-cache` is not optional caution: Docker layer caching silently serves
stale code after repository changes, and this has repeatedly cost debugging
time in this project. Use it whenever repository contents have changed.

Confirm the agent is running:

```bash
docker compose ps && docker logs -f clarity_omega
```

You should see cycle activity in the log. Once the Mattermost values are set,
Clarity will begin participating in her channel.

---

## 5. Everyday operation

| Action | Command |
|---|---|
| Follow the live log | `docker logs -f clarity_omega` |
| Search the log | `docker logs clarity_omega 2>&1 \| grep -E "pattern"` |
| Inspect the live runtime | `docker exec clarity_omega <command>` |
| Stop | `docker compose down` |
| Restart after a code change | `docker compose build --no-cache && docker compose up -d` |

**The live container is ground truth.** `docker run --rm <image>` reads the
baked image copy, not what the running container executes. To inspect what is
actually live, use `docker exec` against the running container.

---

## 6. Verifying it works

There is no automated behavioural test suite, and there cannot easily be one:
soul evaluation and NAL reduction reduce only inside the live loop process.
A standalone `run.sh` invocation starts an empty AtomSpace and is **not**
equivalent to the running system.

Practical checks:

1. **The loop is cycling.** `docker logs -f clarity_omega` shows repeated cycle
   activity rather than a stalled or crash-looping container.
2. **The agent responds.** Send a message in the configured Mattermost channel
   and confirm a reply.
3. **The substrate is populated.** Query the live AtomSpace through
   `docker exec` and confirm awareness-organ atoms such as `recent-action`
   are being written each cycle.

If the container restarts repeatedly, check `.env` first: a missing or invalid
provider key is the most common cause.

---

## 7. Repository layout

| Path | What it holds |
|---|---|
| `src/loop.metta` | The runtime heartbeat. Hooks only, no logic. |
| `src/helper.py` | Python bridge: LLM calls, I/O, ChromaDB, OS operations. |
| `soul/` | The value substrate: MeTTa atoms, evaluation, awareness organs. |
| `lib_clarity_reasoning/` | Reasoning library manifest and imports. |
| `channels/` | Communication channel adapters, including Mattermost. |
| `docs/` | Design record: architecture specs, sprints, investigations. |
| `staging/` | Development scratch: apply scripts, diagnostics, probes, logs. Not required to run the system. |
| `volumes/` | Runtime state, including seed memory. |

---

## 8. Getting help

Open an issue at
[github.com/Berton-C/ClarityOmega/issues](https://github.com/Berton-C/ClarityOmega/issues).
Include what you ran, what you expected, and the relevant lines from
`docker logs clarity_omega`.
