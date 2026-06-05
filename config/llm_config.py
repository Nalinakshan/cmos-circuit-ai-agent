import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
LLM_CONFIG = {
    "model": os.getenv("MODEL_TYPE", "gpt-4"),
    "temperature": float(os.getenv("TEMPERATURE", 0.7)),
    "api_key": os.getenv("OPENAI_API_KEY"),
}

# SPICE Simulator Configuration
SPICE_CONFIG = {
    "simulator": os.getenv("SPICE_SIMULATOR", "ltspice"),
    "process_node": os.getenv("PROCESS_NODE", "130nm"),
}

# Agent Configuration
AGENT_CONFIG = {
    "verbose": True,
    "max_iterations": 10,
    "tools_timeout": 30,
}
