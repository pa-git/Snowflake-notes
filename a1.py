┌──────────────────────────────────────────────┐
│               User Query / Goal              │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│        High-Level Orchestrator / Planner      │
│  (CrewAI, LangGraph, AutoGPT, etc.)           │
│  • Breaks big tasks into smaller subgoals     │
│  • Routes control between agents or nodes     │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│               Memory & Context               │
│  • Conversation history                      │
│  • Retrieved knowledge (RAG)                 │
│  • Tool results and state                    │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│              ReAct Core Loop                 │
│     Thought → Action → Observation → Thought  │
│  • Model reasons about what to do next        │
│  • Executes tool calls or API functions       │
│  • Integrates results into next reasoning step│
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│                Tool Layer                    │
│  • Search, calculator, database, APIs, etc.   │
│  • Each tool has schema + structured I/O      │
└──────────────────────────────────────────────┘
                        │
                        ▼
┌──────────────────────────────────────────────┐
│               Output Synthesizer             │
│  • Summarizes results                        │
│  • Produces final response or report          │
└──────────────────────────────────────────────┘
