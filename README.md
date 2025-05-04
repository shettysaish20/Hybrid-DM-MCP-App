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
## My User Queries Tested

- **What are Tesla's arguments for patent protection? Use local documents and summarize.**

    Logs:
    ```
    🧑 What do you want to solve today? → What are Tesla's arguments for patent protection? Use local documents and summarize.
    `🔁 Step 1/3 starting...
    2025-05-04 20:02:13,690 - modules.history_manager - INFO - Searching conversation history for: What are Tesla's arguments for...
    2025-05-04 20:02:13,690 - modules.history_manager - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide', 'power', 'cbrt', 'factorial', 'remainder', 'sin', 'cos', 'tan', 'mine', 'create_thumbnail', 'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers', 'search_stored_documents', 'convert_webpage_url_into_markdown', 'extract_pdf', 'duckduckgo_search_results', 'download_raw_html_from_url', 'get_current_conversations', 'search_historical_conversations']
    2025-05-04 20:02:14,285 - modules.history_manager - INFO - Found 0 matching conversations
    2025-05-04 20:02:14,285 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:18,450 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:18,455 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:02:18] [perception] Raw output: {
    "intent": "Research and summarize Tesla's arguments for patent protection using local documents.",
    "entities": [
        "Tesla",
        "patent protection"
    ],
    "tool_hint": "document summarization",
    "selected_servers": [
        "documents"
    ]
    }
    result {'intent': "Research and summarize Tesla's arguments for patent protection using local documents.", 'entities': ['Tesla', 'patent protection'], 'tool_hint': 'document summarization', 'selected_servers': ['documents']}
    [perception] intent="Research and summarize Tesla's arguments for patent protection using local documents." entities=['Tesla', 'patent protection'] tool_hint='document summarization' tags=[] selected_servers=['documents']
    2025-05-04 20:02:18,457 - modules.history_manager - INFO - Using cached results for query: What are Tesla's arguments for...
    2025-05-04 20:02:18,460 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:20,096 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:20,096 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:02:20,099 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: line 1 column 1 (char 0)']
    [plan] import json
    async def solve():
        # FUNCTION_CALL: 1
        """Search documents to get relevant extracts. Usage: input={"input": {"query": "your query"}} result = await mcp.call_tool('search_stored_documents', input)"""
        input = {"input": {"query": "Tesla's arguments for patent protection"}}
        result = await mcp.call_tool('search_stored_documents', input)
        return f"FURTHER_PROCESSING_REQUIRED: {result.content[0].text}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()
    [20:02:25] [loop] 🔁 Continuing based on FURTHER_PROCESSING_REQUIRED — Step 1 continues...
    🔁 Step 2/3 starting...
    2025-05-04 20:02:25,607 - modules.history_manager - INFO - Searching conversation history for: Original user task: What are T...      
    2025-05-04 20:02:25,607 - modules.history_manager - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide', 'power', 'cbrt', 'factorial', 'remainder', 'sin', 'cos', 'tan', 'mine', 'create_thumbnail', 'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers', 'search_stored_documents', 'convert_webpage_url_into_markdown', 'extract_pdf', 'duckduckgo_search_results', 'download_raw_html_from_url', 'get_current_conversations', 'search_historical_conversations']
    2025-05-04 20:02:26,121 - modules.history_manager - INFO - Found 0 matching conversations
    2025-05-04 20:02:26,121 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:28,167 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:28,167 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:02:28] [perception] Raw output: {
    "intent": "Summarize Tesla's arguments for patent protection based on provided document.",
    "entities": [
        "Tesla",
        "patent protection"
    ],
    "tool_hint": "This is a summarization task from a local document.",
    "selected_servers": [
        "documents"
    ]
    }
    result {'intent': "Summarize Tesla's arguments for patent protection based on provided document.", 'entities': ['Tesla', 'patent protection'], 'tool_hint': 'This is a summarization task from a local document.', 'selected_servers': ['documents']}
    [perception] intent="Summarize Tesla's arguments for patent protection based on provided document." entities=['Tesla', 'patent protection'] tool_hint='This is a summarization task from a local document.' tags=[] selected_servers=['documents']
    2025-05-04 20:02:28,174 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:31,230 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:31,233 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:02:31,235 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: line 1 column 1 (char 0)']
    [plan] async def solve():
        # The provided document discusses Tesla's arguments against patent protection, specifically their decision to open-source their patents.  It also mentions some potential issues with enforcing this open-source approach. To get a more comprehensive view of their arguments *for* patent protection (if any exist), I will perform a search.
        """Search documents to get relevant extracts. Usage: input={"input": {"query": "your query"}} result = await mcp.call_tool('search_stored_documents', input)"""
        input = {"input": {"query": "Tesla's arguments for patent protection"}}
        result = await mcp.call_tool('search_stored_documents', input)
        return f"FURTHER_PROCESSING_REQUIRED: {result.content[0].text}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()
    [20:02:35] [loop] 🔁 Continuing based on FURTHER_PROCESSING_REQUIRED — Step 2 continues...
    🔁 Step 3/3 starting...
    2025-05-04 20:02:35,615 - modules.history_manager - INFO - Using cached results for query: Original user task: What are T...
    2025-05-04 20:02:35,615 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:38,096 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:38,096 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:02:38] [perception] Raw output: {
    "intent": "Summarize Tesla's arguments for patent protection based on a provided document and potentially find more information.",  
    "entities": [
        "Tesla",
        "patent protection",
        "patent infringement"
    ],
    "tool_hint": "Summarization tool to condense the document further.",
    "selected_servers": [
        "documents"
    ]
    }
    result {'intent': "Summarize Tesla's arguments for patent protection based on a provided document and potentially find more information.", 'entities': ['Tesla', 'patent protection', 'patent infringement'], 'tool_hint': 'Summarization tool to condense the document further.', 'selected_servers': ['documents']}
    [perception] intent="Summarize Tesla's arguments for patent protection based on a provided document and potentially find more information." entities=['Tesla', 'patent protection', 'patent infringement'] tool_hint='Summarization tool to condense the document further.' tags=[] selected_servers=['documents']
    2025-05-04 20:02:38,103 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:02:42,553 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:02:42,555 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:02:42,555 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: `line 1 column 1 (char 0)']
    [plan] async def solve():
    # The provided document discusses Tesla's arguments for open-sourcing their patents rather than traditional patent protection.    
    # It mentions that Tesla's move was intended to inspire others and that it was seen as a positive step by the patent reform movement.
    # However, it also raises questions about the enforceability of Tesla's promise not to sue for patent infringement, especially if Tesla were to be sold or go bankrupt.
    # It suggests that the courts would ultimately have to resolve these issues.

    # The question asks for Tesla's arguments for patent protection, but the document primarily discusses their arguments for *not* using traditional patent protection. Therefore, I can extract the information from the provided document and reframe it to answer the question.
    text = """Tesla's arguments for foregoing traditional patent protection include:
    - To encourage innovation and collaboration in the electric vehicle industry.
    - To accelerate the development of sustainable transportation.
    - A belief that open-sourcing their patents would inspire other companies to follow suit.

    The document also raises concerns about the potential downsides of open-sourcing, such as enforceability and the possibility of future patent assertion by third parties, should Tesla be sold or go bankrupt."""

    return f"FINAL_ANSWER: {text}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()

    💡 Final Answer: Tesla's arguments for foregoing traditional patent protection include:
        - To encourage innovation and collaboration in the electric vehicle industry.
        - To accelerate the development of sustainable transportation.
        - A belief that open-sourcing their patents would inspire other companies to follow suit.

        The document also raises concerns about the potential downsides of open-sourcing, such as enforceability and the possibility of future patent assertion by third parties, should Tesla be sold or go bankrupt.
    ```

- **Summarize this news article for me in 50 words https://www.bbc.com/news/articles/cg72x3dd7ydo**

    Logs:
    ```
    🧑 What do you want to solve today? → Summarize this news article for me in 50 words https://www.bbc.com/news/articles/cg72x3dd7ydo
    🔁 Step 1/3 starting...
    2025-05-04 20:07:25,584 - modules.history_manager - INFO - Searching conversation history for: Summarize this news article fo...
    2025-05-04 20:07:25,584 - modules.history_manager - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide', 'power', 'cbrt', 'factorial', 'remainder', 'sin', 'cos', 'tan', 'mine', 'create_thumbnail', 'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers', 'search_stored_documents', 'convert_webpage_url_into_markdown', 'extract_pdf', 'duckduckgo_search_results', 'download_raw_html_from_url', 'get_current_conversations', 'search_historical_conversations']
    2025-05-04 20:07:26,221 - modules.history_manager - INFO - Found 0 matching conversations
    2025-05-04 20:07:26,221 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:07:27,395 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:07:27,397 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:07:27] [perception] Raw output: {
    "intent": "Summarize a news article",
    "entities": [
        "news article",
        "summary",
        "https://www.bbc.com/news/articles/cg72x3dd7ydo"
    ],
    "tool_hint": "webpage summarization",
    "selected_servers": [
        "documents",
        "websearch"
    ]
    }
    result {'intent': 'Summarize a news article', 'entities': ['news article', 'summary', 'https://www.bbc.com/news/articles/cg72x3dd7ydo'], 'tool_hint': 'webpage summarization', 'selected_servers': ['documents', 'websearch']}
    [perception] intent='Summarize a news article' entities=['news article', 'summary', 'https://www.bbc.com/news/articles/cg72x3dd7ydo'] tool_hint='webpage summarization' tags=[] selected_servers=['documents', 'websearch']
    2025-05-04 20:07:27,397 - modules.history_manager - INFO - Using cached results for query: Summarize this news article fo...
    2025-05-04 20:07:27,400 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:07:30,205 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:07:30,207 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:07:30,209 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: line 1 column 1 (char 0)']
    [plan] async def solve():
        # FUNCTION_CALL: 1
        """Return clean webpage content without Ads, and clutter. Usage: input={{"input": {{"url": "https://example.com"}}}} result = await mcp.call_tool('convert_webpage_url_into_markdown', input)"""
        input = {"input": {"url": "https://www.bbc.com/news/articles/cg72x3dd7ydo"}}
        result = await mcp.call_tool('convert_webpage_url_into_markdown', input)
        return f"FURTHER_PROCESSING_REQUIRED: {result.content[0].text}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()
    [20:07:32] [loop] 🔁 Continuing based on FURTHER_PROCESSING_REQUIRED — Step 1 continues...
    🔁 Step 2/3 starting...
    2025-05-04 20:07:32,261 - modules.history_manager - INFO - Searching conversation history for: Original user task: Summarize ...      
    2025-05-04 20:07:32,261 - modules.history_manager - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide', 'power', 'cbrt', 'factorial', 'remainder', 'sin', 'cos', 'tan', 'mine', 'create_thumbnail', 'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers', 'search_stored_documents', 'convert_webpage_url_into_markdown', 'extract_pdf', 'duckduckgo_search_results', 'download_raw_html_from_url', 'get_current_conversations', 'search_historical_conversations']
    2025-05-04 20:07:32,886 - modules.history_manager - INFO - Found 0 matching conversations
    2025-05-04 20:07:32,886 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:07:36,632 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:07:36,633 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:07:36] [perception] Raw output: {
    "intent": "Summarize a news article.",
    "entities": [
        "news article",
        "Australia's opposition election defeat",
        "50 words"
    ],
    "tool_hint": "No tool needed, the markdown already contains the summarized article",
    "selected_servers": []
    }
    result {'intent': 'Summarize a news article.', 'entities': ['news article', "Australia's opposition election defeat", '50 words'], 'tool_hint': 'No tool needed, the markdown already contains the summarized article', 'selected_servers': []}
    [perception] intent='Summarize a news article.' entities=['news article', "Australia's opposition election defeat", '50 words'] tool_hint='No tool needed, the markdown already contains the summarized article' tags=[] selected_servers=[]
    [20:07:36] [loop] ⚠️ No tools selected — aborting step.
    🔁 Step 3/3 starting...
    2025-05-04 20:07:36,633 - modules.history_manager - INFO - Using cached results for query: Original user task: Summarize ...
    2025-05-04 20:07:36,634 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:07:37,853 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:07:37,857 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:07:37] [perception] Raw output: {
    "intent": "Summarize a news article.",
    "entities": [
        "news article",
        "summary",
        "50 words"
    ],
    "tool_hint": "The document summarization can likely be improved.",
    "selected_servers": [
        "documents"
    ]
    }
    result {'intent': 'Summarize a news article.', 'entities': ['news article', 'summary', '50 words'], 'tool_hint': 'The document summarization can likely be improved.', 'selected_servers': ['documents']}
    [perception] intent='Summarize a news article.' entities=['news article', 'summary', '50 words'] tool_hint='The document summarization can likely be improved.' tags=[] selected_servers=['documents']
    2025-05-04 20:07:37,860 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:07:42,427 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:07:42,430 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:07:42,430 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: line 1 column 1 (char 0)']
    [plan] async def solve():
        article_text = "# Australia's opposition left reeling after crushing election defeat\n\nAustralia's opposition party has been left reeling after a bruising defeat in Saturday's federal election, with a result that is shaping up to be its worst ever loss.\n\nPeter Dutton, the Liberal party leader, also lost his own seat of Dickson, which he had held for the past 24 years.\n\nLabor's landslide victory means the Liberal party is now scrambling to find a new leader - and figure out what went wrong for them this election cycle.\n\nSome Liberal party members have called for a \"serious review\", with one adviser summing up the loss as a failure of \"the Dutton experiment\".\n\nDutton has also become the first federal opposition leader to ever lose their own seat at the same time as losing an election, which means he has been ousted from parliament.\n\nLabor's Ali France defeated Dutton in his home base of Dickson in Queensland.\n\nIn his first public appearance after Labor's emphatic win, prime minister Anthony Albanese told media outside a Sydney cafe on Sunday that \"the Australian people voted for unity rather than division\".\n\nThe Liberal party's most crushing losses were in Australia's major cities, where party members have been all but wiped out in metropolitan areas including Sydney, Melbourne, Brisbane and Adelaide.\n\nLiberal MP Keith Wolahan has called for a \"serious review\" of the systemic issues that led to the party's shock defeat.\n\n\"You have to acknowledge things went wrong,\" he told the Australian Broadcasting Corporation's Insiders program.\n\n\"We have to listen to Australians. They have sent us a message, and our first task is to hear it. And that often takes time.\"\n\nWolahan represents the seat of Menzies in Victoria, and said it was very likely he would also lose his seat.\n\nWhen asked if Peter Dutton himself was the problem, Wolahan declined to answer directly, but said he has great respect for the Liberal leader.\n\nSome were more blunt, like Andrew Carswell, a former adviser to Australia's last Liberal prime minister, who told the ABC \"the Dutton experiment failed\".\n\nHe went on to describe Saturday's loss as \"a complete catastrophe for the Coalition\", which he said showed that Australians had \"clear hesitation with Peter Dutton\".\n\nThe looming presence of Donald Trump has also been cited as a major factor for thwarting Dutton's already inconsistent campaign, with many people drawing parallels between him and the American president.\n\nDutton's loss has now set in motion the scramble for a new Liberal party leader.\n\nCarswell was hopeful about the prospect of some \"very good up-and-coming Liberal MPs\" stepping into leadership roles.\n\nThose tipped as most likely contenders for the top job include shadow treasurer Angus Taylor and deputy leader Sussan Ley.\n\nShadow immigration minister Dan Tehan and shadow minister of defence Andrew Hastie have also been mentioned.\n\nBut without a clear frontrunner, the Liberal party will have to try to regroup in the coming days - as well as develop a new strategy to win back the voters they lost."
        summary = "Australia's Liberal party faces a leadership vacuum after a crushing election defeat, with leader Peter Dutton losing his seat. The party suffered major losses in cities, prompting calls for a 'serious review' and criticism of the 'Dutton experiment'. Potential leaders include Angus Taylor and Sussan Ley."
        return f"FINAL_ANSWER: {summary}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()

    💡 Final Answer: Australia's Liberal party faces a leadership vacuum after a crushing election defeat, with leader Peter Dutton losing his seat. The party suffered major losses in cities, prompting calls for a 'serious review' and criticism of the 'Dutton experiment'. Potential leaders include Angus Taylor and Sussan Ley.
    ```

- **Find the sum of first 10 fibonacci numbers**

    Logs:
    ```
    🧑 What do you want to solve today? → Find the sum of first 10 fibonacci numbers
    🔁 Step 1/3 starting...
    2025-05-04 20:09:07,069 - modules.history_manager - INFO - Searching conversation history for: Find the sum of first 10 fibon...
    2025-05-04 20:09:07,069 - modules.history_manager - INFO - Available tools: ['add', 'subtract', 'multiply', 'divide', 'power', 'cbrt', 'factorial', 'remainder', 'sin', 'cos', 'tan', 'mine', 'create_thumbnail', 'strings_to_chars_to_int', 'int_list_to_exponential_sum', 'fibonacci_numbers', 'search_stored_documents', 'convert_webpage_url_into_markdown', 'extract_pdf', 'duckduckgo_search_results', 'download_raw_html_from_url', 'get_current_conversations', 'search_historical_conversations']
    2025-05-04 20:09:07,646 - modules.history_manager - INFO - Found 0 matching conversations
    2025-05-04 20:09:07,646 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:09:09,610 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:09:09,615 - google_genai.models - INFO - AFC remote call 1 is done.
    [20:09:09] [perception] Raw output: {
    "intent": "Calculate the sum of the first 10 Fibonacci numbers.",
    "entities": [
        "Fibonacci numbers",
        "sum",
        "10"
    ],
    "tool_hint": "python sandbox",
    "selected_servers": [
        "math"
    ]
    }
    result {'intent': 'Calculate the sum of the first 10 Fibonacci numbers.', 'entities': ['Fibonacci numbers', 'sum', '10'], 'tool_hint': 'python sandbox', 'selected_servers': ['math']}
    [perception] intent='Calculate the sum of the first 10 Fibonacci numbers.' entities=['Fibonacci numbers', 'sum', '10'] tool_hint='python sandbox' tags=[] selected_servers=['math']
    2025-05-04 20:09:09,615 - modules.history_manager - INFO - Using cached results for query: Find the sum of first 10 fibon...
    2025-05-04 20:09:09,617 - google_genai.models - INFO - AFC is enabled with max remote calls: 10.
    2025-05-04 20:09:10,993 - httpx - INFO - HTTP Request: POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent "HTTP/1.1 200 OK"
    2025-05-04 20:09:10,995 - google_genai.models - INFO - AFC remote call 1 is done.
    2025-05-04 20:09:10,996 - root - WARNING - Output validation issues: ['Invalid JSON format: Expecting value: line 1 column 1 (char 0)']
    [plan] import json
    async def solve():
        # FUNCTION_CALL: 1
        """Generate first n Fibonacci numbers. Usage: input={"input": {"n": 10}} result = await mcp.call_tool('fibonacci_numbers', input)"""
        input = {"input": {"n": 10}}
        result = await mcp.call_tool('fibonacci_numbers', input)
        fibonacci_numbers = json.loads(result.content[0].text)["result"]
        sum_fibonacci = sum(fibonacci_numbers)
        return f"FINAL_ANSWER: {sum_fibonacci}"
    [loop] Detected solve() plan — running sandboxed...
    [action] 🔍 Entered run_python_sandbox()

    💡 Final Answer: 88
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
