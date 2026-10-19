# Hello World AI Agent

A Python AI agent that greets users by name, demonstrating the agent framework and serving as a reusable template for future agent development.

## Business challenge

Development teams need a minimal, working AI agent example to understand the agent framework, reduce onboarding friction, and accelerate future agent projects by providing a proven starting point.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Developer onboarding time for new agent projects | — | 50% reduction | — | Agent framework adoption | user |

## Key Milestones

1. **Agent initialized** — Agent project structure is bootstrapped and dependencies are installed.
2. **Name received** — Agent successfully receives and parses a user's name from an incoming message.
3. **Greeting generated** — Agent produces a personalized greeting response using the LLM.
4. **Response returned** — Agent returns the greeting to the caller via the A2A protocol.
5. **Tests pass** — All unit and prebuilt tests pass, confirming the template is production-ready.

## Business Architecture (RBA)

### End-to-End Process

Governance (IT Management)

### Process Hierarchy

```
Governance (IT Management)
└── Manage Information Technology (generic)
    └── Manage IT business strategy (generic) (BPS-455)
        └── Manage IT Portfolio and Operating Model
    └── Manage IT governance (generic) (BPS-456)
        └── Operate IT Governance Framework
```

### Summary

Building a reusable agent template maps to IT governance and digital asset management — specifically managing the development and lifecycle of reusable digital assets (agent templates) as part of an IT operating model.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|------------------------|------------|-------------------|-------------------|-------------------|---------------------|------|---------------------|
| AI agent framework with user greeting | None | — | — | — | — | — | Yes | All discovered APIs are unavailable in this landscape; full custom build required |
| Reusable agent template structure | None | — | — | — | — | — | Yes | Custom Python agent (A2A protocol) covers this gap |

### Key findings

- No standard SAP product covers the "hello world" agent use case out of the box.
- All AI/agent-related APIs discovered are marked unavailable in this landscape.
- The solution is a fully custom Python AI agent using the A2A protocol and agent framework templates.
- The agent serves dual purpose: functional demo (greeting by name) and developer template.
- OpenTelemetry instrumentation should be included to establish observability best practices from the start.

## Recommendations

### Hello World AI Agent as Reusable Template

#### Executive Summary

Custom Python A2A agent demonstrating framework with personalized greeting.

#### Recommended Solution

Build a pro-code Python AI agent using the A2A protocol. The agent accepts a user's name as input, uses an LLM to generate a personalized greeting, and returns it. The project includes full test coverage, OpenTelemetry instrumentation stubs, and a clean structure that teams can clone for future agents.

#### Recommended solution category

AI Agent

#### Intent fit
95%
