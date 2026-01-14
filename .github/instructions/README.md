# GitHub Agent Instructions

This directory contains instructions for various AI agents working on this repository.

## Files in This Directory

### copilot-instructions.md
**Primary File**: Strict coding standards for GitHub Copilot

Contains:
- TypeScript strict mode requirements (no `any` types)
- React component standards
- Tailwind CSS styling rules
- Naming conventions
- Error handling patterns
- Accessibility requirements
- Git commit message format

**Target Audience**: GitHub Copilot, code completion tools

## Relationship to Other Documentation

```
Repository Root
├── AGENTS.md                          # AI agent coordination guide
├── GEMINI.md                          # Gemini vision & architecture
└── .github/
    └── instructions/
        └── copilot-instructions.md    # Copilot strict standards (symlinked to parent)
```

### Document Hierarchy

1. **AGENTS.md** - Coordination protocol between AI agents
2. **GEMINI.md** - High-level vision and architecture
3. **copilot-instructions.md** - Tactical coding standards

## Adding New Agent Instructions

When adding instructions for a new agent:

1. Create `[agent-name]-instructions.md` in this directory
2. Reference the coordination protocol in `AGENTS.md`
3. Be specific about the agent's role and responsibilities
4. Include code examples where appropriate
5. Update this README with the new file

## Usage

### For AI Agents
Read the appropriate instructions file before starting work:
- **Gemini**: Read `AGENTS.md` and `GEMINI.md`
- **Copilot**: Read `.github/copilot-instructions.md`
- **Other agents**: Read `AGENTS.md` for coordination protocol

### For Developers
These files document coding standards and architectural decisions. Useful for:
- Understanding project conventions
- Onboarding new team members
- Reviewing PR compliance with standards

---

For specification-driven development workflow, see `/docs/specs/README.md`.
