
from langgraph.types import interrupt
from langchain.tools import tool

@tool
def listContainers() -> str:
    """list all running docker containers with name, Id, status and memory usage"""
    import subprocess
    result = subprocess.run(["docker", "ps", "--format", "{{.Names}}\t{{.ID}}\t{{.Status}}\t{{.Size}}"], capture_output=True, text=True)
    
    return result.stdout.strip() or result.stderr.strip() or "No output from docker command."

@tool
def getContainerStats(container_id: str) -> str:
    """get the stats of a docker container by its ID"""
    import subprocess
    result = subprocess.run(["docker", "stats", container_id, "--no-stream", "--format", "{{.Name}}\t{{.ID}}\t{{.CPUPerc}}\t{{.MemUsage}}"], capture_output=True, text=True)
    
    return result.stdout.strip() or result.stderr.strip() or "No output from docker command."

@tool
def restartContainer(container_name: str) -> str:
    """restart a docker container by its name"""
    
    confirmation = interrupt("Are you sure you want to restart the container with name: " + container_name + "? (yes/no)")
    if confirmation != "yes":
        return "Container restart cancelled by user."
    
    import subprocess
    result = subprocess.run(["docker", "restart", container_name], capture_output=True, text=True)
    
    return f"restrated container : {container_name} with result: " + (result.stdout.strip() or result.stderr.strip() or "No output from docker command.")   

@tool
def killContainer(container_name: str) -> str:
    """kill a docker container by its name"""
    
    confirmation = interrupt("Are you sure you want to kill the container with name: " + container_name + "? (yes/no)")
    if confirmation != "yes":
        return "Container kill cancelled by user."
    
    import subprocess
    result = subprocess.run(["docker", "kill", container_name], capture_output=True, text=True)
    
    return f"killed container : {container_name} with result: " + (result.stdout.strip() or result.stderr.strip() or "No output from docker command.")   





