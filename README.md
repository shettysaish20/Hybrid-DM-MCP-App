# Cortex-R: Multi-MCP Agent App 🤖🧠

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python)](https://www.python.org/) [![LLM](https://img.shields.io/badge/LLM-Ready-brightgreen?logo=openai)](https://platform.openai.com/) [![RAG](https://img.shields.io/badge/RAG-Enabled-orange)]() [![Heuristics](https://img.shields.io/badge/Heuristics-Input%2FOutput%20Validation-yellow)]() [![MCP](https://img.shields.io/badge/MCP-Multi--Server-purple)]()

---

## 🚀 Overview

**Cortex-R** is a reasoning-driven, multi-MCP (Model Context Protocol) agent app designed for controlled, effective LLM (Large Language Model) generation. It leverages:
- **Strategic prompt engineering** (conservative, exploratory, fallback, etc.)
- **Input/output validation heuristics** for safe, robust LLM calls
- **Multi-server orchestration** for tool-rich, modular, and scalable agentic workflows
- **Memory and context management** for stepwise, context-aware problem solving

> "A modular, tool-using agent that plans, validates, and executes with precision."

---

## ✨ Features
- 🧩 **Multi-MCP Server Orchestration**: Math, document, web, and memory servers
- 🛡️ **Heuristic Input/Output Validation**: NSFW, length, format, and schema checks
- 🧠 **Strategic Prompting**: Conservative, parallel, sequential, and fallback plans
- 📚 **RAG & Document Search**: FAISS-based semantic search over local and web docs
- 📝 **Session Memory**: Date-structured, persistent memory for context and history
- 🔧 **Extensible Tooling**: Add new tools and servers with minimal code changes

---

## 📂 Directory Structure

```
Hybrid-MCP-App/
├── agent.py                # Main agent entrypoint
├── heuristics.py           # Input/output validation heuristics
├── mcp_server_1.py         # Math & utility MCP server
├── mcp_server_2.py         # Document & RAG MCP server
├── mcp_server_3.py         # Web search MCP server
├── mcp_server_check.py     # MCP server test script
├── models.py               # Pydantic models for tool schemas
├── pyproject.toml          # Python project config
├── uv.lock                 # Dependency lock file
├── config/
│   ├── models.json         # Model configs
│   └── profiles.yaml       # Agent, strategy, and server configs
├── core/
│   ├── context.py          # Agent context/session
│   ├── loop.py             # Main agent loop
│   ├── session.py          # MCP session management
│   └── strategy.py         # Planning strategies
├── modules/
│   ├── action.py           # Tool execution logic
│   ├── decision.py         # Planning/decision logic
│   ├── history_manager.py  # Conversation history
│   ├── model_manager.py    # LLM model abstraction
│   ├── perception.py       # Perception extraction
│   └── tools.py            # Tool utilities
├── prompts/
│   ├── decision_prompt.txt
│   ├── decision_prompt_conservative.txt
│   ├── decision_prompt_exploratory_parallel.txt
│   ├── decision_prompt_exploratory_sequential.txt
│   ├── decision_prompt_new.txt
│   └── perception_prompt.txt
├── documents/              # Local docs for RAG
├── faiss_index/            # FAISS semantic index
├── memory/                 # Date-structured session memory
└── ...
```

---

## 🛠️ How It Works
1. **Perception**: Extracts intent, entities, and relevant servers from user input
2. **Planning**: Selects a prompt strategy (conservative, parallel, sequential)
3. **Validation**: Applies heuristics to all LLM inputs/outputs
4. **Execution**: Runs tool calls via MCP servers, with fallback and memory
5. **Memory**: Stores and retrieves session context for better reasoning

---

## 📦 Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Start an MCP server (example)
python mcp_server_1.py

# Run the agent
python agent.py
```

---

## 📑 Example Prompts & Strategies
- **Conservative**: One tool call, strict validation
- **Exploratory (Parallel)**: Multiple independent tool calls
- **Exploratory (Sequential)**: Fallbacks if previous tool fails
- **RAG**: Search and summarize local/web documents

See `prompts/` for real prompt templates and examples.

---

## 🧩 Extending
- Add new tools to any `mcp_server_X.py`
- Add new prompt strategies in `prompts/`
- Add new heuristics in `heuristics.py`

---

## 📝 License
MIT License

---

## 🙏 Acknowledgements
- [MCP Protocol](https://github.com/theschoolofai/mcp)
- [FAISS](https://github.com/facebookresearch/faiss)
- [Gemini, Ollama, etc.]

---

> Made with ❤️ for robust, agentic LLM workflows.
