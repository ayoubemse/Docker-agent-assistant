from langgraph.types import Command

def stream_model_text(agent, payload, config):
    """Stream the model's textual output; ignore tool_use / deltas. Returns collected text."""
    collected = []
    for chunk, metadata in agent.stream(
        payload, config=config, stream_mode="messages"
    ):
        if metadata.get("langgraph_node") != "model":
            continue
        content = getattr(chunk, "content", None)
        if isinstance(content, str):
            if content:
                print(content, end="", flush=True)
                collected.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        print(text, end="", flush=True)
                        collected.append(text)
    print()
    return "".join(collected)


def pending_interrupt_prompt(state):
    """Return the prompt string from the first pending interrupt, or None."""
    for task in getattr(state, "tasks", []) or []:
        for itr in getattr(task, "interrupts", []) or []:
            value = getattr(itr, "value", itr)
            return "" if value is None else str(value)
    return None


def _ask(prompt):
    while True:
        try:
            answer = input(prompt).strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            return "no"
        if answer in ("yes", "y"):
            return "yes"
        if answer in ("no", "n"):
            return "no"
        print("Please type 'yes' or 'no'.")


def run_agent(agent, user_input, config):
    print("Agent: ", end="", flush=True)

    state = agent.get_state(config)
    if pending_interrupt_prompt(state) is not None:
        try:
            stream_model_text(agent, Command(resume="no"), config)
        except Exception as e:
            print(f"[recovering from stale interrupt: {e}]")

    payload = {"messages": [{"role": "user", "content": user_input}]}

    result = ""
    while True:
        result = stream_model_text(agent, payload, config)

        state = agent.get_state(config)
        prompt = pending_interrupt_prompt(state)
        if prompt is None:
            return result  # graph finished cleanly

        print(f"\n⚠️  {prompt}")
        answer = _ask("Confirm? (yes/no): ")
        payload = Command(resume=answer)
        print("Agent: ", end="", flush=True)


def main():
    print("Docker Agent CLI ready")
    config = {"configurable": {"thread_id": "docker-agent-thread"}}
    run_agent(agent, "List all running docker containers.", config=config)

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if user_input.lower() in ("exit", "quit", "q"):
            print("Exiting Docker Agent CLI.")
            break
        if not user_input.strip():
            continue
        run_agent(agent, user_input, config=config)


if __name__ == "__main__":
    main()
