# HoloOS v0.8.0
Super Intelligence Native AI Operating System

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python holoos/main.py
```

## Web Interface

Open `holoos/index.html` in your browser.

## Modules (20+)

### Core Modules (17)
- **AI Hub** - 17 AI models (GPT-4, Claude, Gemini, Llama, etc.)
- **Kernel** - Self-Attention + Soul + Consciousness
- **Security** - Auto-defense, threat detection
- **Memory** - Vector, episodic, working, procedural
- **Planner** - Goals, reasoning (CoT, ToT, ReAct)
- **Tools** - 9 executable tools
- **Gateway** - Rate limiting, auth
- **Database** - SQL, NoSQL, Key-Value
- **Monitoring** - Metrics, health checks
- **Plugins** - Dynamic loading
- **Config** - Environment management
- **Governance** - Multi-agent assembly
- **Quantizer** - LLM quantization
- **Transpiler** - Multi-language
- **Agent** - AI agents
- **Distributed** - Distributed execution
- **Generator** - Autonomous code generation

### New in v0.8.0 🆕
- **Event Bus** - Pub/sub system for inter-module communication
- **RAG Engine** - Retrieval-Augmented Generation with embeddings
- **Orchestration** - Multi-agent collaboration
- **Integrations**:
  - **LangChain Adapter** - Use HoloOS tools in LangChain
  - **ChromaDB** - Vector database integration
  - **Prometheus** - Metrics export for observability

## Quick Start - Integrations

### Using Event Bus
```python
from holoos import get_event_bus, publish_event, EventType

# Subscribe to events
event_bus = get_event_bus()
event_bus.subscribe("memory.*", lambda e: print(f"Memory event: {e.payload}"))

# Publish events
publish_event(
    topic="memory.write",
    payload={"key": "test", "value": "data"},
    event_type=EventType.MEMORY_WRITE,
    source="app"
)
```

### Using LangChain Adapter
```python
from holoos import get_langchain_adapter

adapter = get_langchain_adapter()
tools = adapter.to_langchain_tools()

# Use with LangChain agents
from langchain.agents import initialize_agent
agent = initialize_agent(tools, llm, agent="zero-shot-react-description")
```

### Using ChromaDB for RAG
```python
from holoos import get_chromadb_rag

rag = get_chromadb_rag(persist_directory="./chroma_data")
rag.add_document("HoloOS is an AI operating system", {"category": "docs"})
results = rag.retrieve("What is HoloOS?", top_k=3)
```

### Exporting Prometheus Metrics
```python
from holoos import get_prometheus_metrics

metrics = get_prometheus_metrics(port=8001)
metrics.start_server()

# Record custom metrics
metrics.record_inference("gpt-4", duration=1.5, tokens=100, success=True)
```

## Status

✅ All systems online
✅ Event Bus operational
✅ LangChain integration ready
✅ ChromaDB integration ready
✅ Prometheus metrics exporter ready

---

Version: 0.8.0
Files: 50+ Python files
Languages: 35+
Integrations: LangChain, ChromaDB, Prometheus