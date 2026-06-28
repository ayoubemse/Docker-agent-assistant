# Docker Agent

A Docker assistant powered by Claude (`claude-sonnet-4-6`) via LangChain / LangGraph. Ask questions in natural language about your containers, or query Docker documentation — the agent calls the right tools on your behalf.

Comes with a web UI and a FastAPI backend. Conversation history persists across server restarts via SQLite.

## Tools

- `listContainers` — list all running containers with name, ID, status, and memory usage
- `getContainerStats` — get CPU and memory stats for a container by ID
- `restartContainer` — restart a container by name *(requires confirmation)*
- `killContainer` — kill a container by name *(requires confirmation)*
- `searchDocs` — search your Docker documentation using RAG (Voyage AI + ChromaDB)

## Prerequisites

- Docker installed and running
- An [Anthropic API key](https://console.anthropic.com/)
- A [Voyage AI API key](https://dash.voyageai.com/)
- Docker documentation PDFs placed in `./data/`

## Setup

**1. Create a `.env` file:**

```
ANTHROPIC_API_KEY=sk-ant-...
VOYAGE_API_KEY=pa-...
```

**2. Add your Docker documentation PDFs to `./data/`**

## Run with Docker Compose

```bash
docker-compose up --build
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Run locally

```bash
pip install -r requirements.txt
python3 api.py
```

## Project structure

```
dockerCLI/
├── api.py              # FastAPI server
├── agent.py            # LangGraph agent setup
├── docker_agent.py     # agent runner (streaming, interrupt handling)
├── tools.py            # tool definitions wrapping docker CLI and RAG
├── rag_experiment.py   # ChromaDB vector store + Voyage AI embeddings
├── static/
│   └── index.html      # web UI
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```
