# Coding Agent Instructions

This project was built with the microsoft-foundry skill. Before working on or answering questions about foundry agents, read the microsoft-foundry skill first.

## Showcase rules

- All Volt and Co products, orders, policies, and results use synthetic data.
- The production-like demo is not customer production.
- Never describe offline fixture results as live model or Azure results.
- Keep secrets out of source, notes, screenshots, traces, and evidence.
- Keep the three domain tools read-only. Do not enable shell, file, network,
  or general coding tools in the customer-facing runtime harness.
- Keep baseline and improved behavior explicit. The baseline intentionally
  demonstrates a missing-batch lookup bug; it must never be treated as production safe.
- Do not weaken evaluation checks to make a demonstration pass.

This project is a **Microsoft Foundry hosted agent** — a containerized AI agent that runs in [Foundry Agent Service](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents). The platform handles containerization, hosting, security, scaling, and observability so you can focus on agent logic.

## Key files

- `Dockerfile` — container definition

## Development workflow

The **Azure Developer CLI (`azd`)** manages the full lifecycle:

```bash
azd ai agent run                           # Run locally on http://localhost:8088
azd ai agent invoke --local "your message" # Test the local agent
azd deploy                                 # Deploy to Foundry
azd ai agent invoke "your message"         # Invoke the deployed agent
```

## Microsoft Foundry Skill

Install the **Microsoft Foundry Skill** for guided deployment, evaluation, and troubleshooting workflows.

Direct install (preferred, works with any coding agent):

```bash
npx skills add https://github.com/microsoft/azure-skills --skill microsoft-foundry
```

Or install the Azure Skills Plugin:

- **Copilot CLI**: `/plugin marketplace add microsoft/azure-skills` then `/plugin install azure@azure-skills`
- **Claude Code**: `/plugin install azure@claude-plugins-official`

Then ask naturally, e.g. `Use the Microsoft Foundry Skill to deploy this agent.`

## References

- [Hosted agents overview](https://learn.microsoft.com/en-us/azure/foundry/agents/concepts/hosted-agents)
- [Microsoft Foundry Skill](https://learn.microsoft.com/en-us/azure/foundry/how-to/develop/use-microsoft-foundry-skill)