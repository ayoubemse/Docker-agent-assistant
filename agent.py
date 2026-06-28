from tools import listContainers, getContainerStats, restartContainer, killContainer, searchDocs
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command
import sqlite3
import os
model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0.3,
    timeout=600,
    max_tokens=25000,
    streaming=True,
)

conn = sqlite3.connect("./conversations.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


SYSTEM_PROMPT = """You are a docker assistant.

## Tools
- `listContainers`: list all running containers with name, ID, status, memory
- `getContainerStats`: get stats for a container by ID
- `restartContainer`: restart a container by name
- `killContainer`: kill a container by name
- 'searchDocs': search for relevant docker documentation based on a query

## Rules
- Always use tools to answer, never guess
- Call tools immediately when needed — do not ask for confirmation, it is handled automatically
- Report exact error messages on failure
- Be concise — this is a CLI tool"""

tools = [listContainers, getContainerStats, restartContainer, killContainer, searchDocs]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

