# docker_agent 🤖

An agent-based CLI tool that acts as a Docker assistant, powered by Claude (`claude-sonnet-4-6`) via LangChain / LangGraph.

You describe what you want in natural language ("list my containers", "restart the one using the most CPU") and the agent calls the right Docker commands on your behalf.

## Tools

The agent exposes the following tools:

- `listContainers` — list all running containers with name, ID, status, and memory usage
- `getContainerStats` — get stats (CPU, memory) for a container by ID
- `restartContainer` — restart a container by name *(requires user confirmation)*
- `killContainer` — kill a container by name *(requires user confirmation)*

Destructive actions (`restartContainer`, `killContainer`) pause execution and prompt for `yes`/`no` confirmation before running.

## Prerequisites

- Python 3.10+
- Docker installed and running (`docker ps` should work in your shell)
- An Anthropic API key — get one at https://console.anthropic.com/

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. (Optional) Make the script executable
chmod +x docker_agent.py
```

## Usage

```bash
python3 docker_agent.py
```

On launch the agent lists your running containers, then drops into an interactive prompt. Type `exit`, `quit`, or `q` to leave.

## Project structure

```
dockerCLI/
├── docker_agent.py   # entry point: model setup, streaming loop, confirmation handling
├── tools.py          # tool definitions wrapping `docker` CLI calls
└── README.md
```

## Example session

```
Docker Agent CLI ready
Agent: Here are the **4 running containers**:

| Name | ID | Status | Memory |
|------|----|--------|--------|
| test-nginx | 5484943b4d2a | ✅ Up 6 days | 81.9 kB |
| test-postgres | 28b929b2907d | ✅ Up 6 days | 20.5 kB |
| test-redis | 2abf1dc5730e | ✅ Up 6 days | 4.1 kB |
| docker-compose-project-node-app-1 | 0e6efc3b6349 | ⚠️ Restarting (exit code 1) | 102 kB |

> ⚠️ **Note:** `docker-compose-project-node-app-1` is in a **crash loop** (exit code 1). You may want to inspect its logs or restart it.

You: restart the container with most cpu
Agent: Let me first get the stats for all containers simultaneously to find the one with the most CPU usage. `test-redis` has the highest CPU usage at **0.31%**. Restarting it now.

⚠️  Are you sure you want to restart the container with name: test-redis? (yes/no)
Confirm? (yes/no): yes
Agent: ✅ **test-redis** has been restarted. It had the highest CPU usage at **0.31%** across all containers.

You: now list all containers again
Agent: Here are the **4 running containers**:

| Name | ID | Status | Memory |
|------|----|--------|--------|
| test-nginx | 5484943b4d2a | ✅ Up 6 days | 81.9 kB |
| test-postgres | 28b929b2907d | ✅ Up 6 days | 20.5 kB |
| test-redis | 2abf1dc5730e | ✅ Up 11 seconds | 12.3 kB |
| docker-compose-project-node-app-1 | 0e6efc3b6349 | ⚠️ Restarting (exit code 1) | 102 kB |

> ✅ **test-redis** is back up and running (11 seconds).
> ⚠️ **docker-compose-project-node-app-1** is still in a crash loop (exit code 1).
```
