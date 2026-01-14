# FileUploads Context Documentation

This directory contains project-specific knowledge, decisions, and patterns that help AI agents and developers understand the codebase.

## Purpose

Context documentation captures the "why" behind architectural decisions, common patterns used in the codebase, and project-specific knowledge that isn't obvious from reading the code.

## Documents in This Directory

### decisions.md
Records major architectural and technical decisions, including:
- What was decided
- Why it was decided
- Alternative approaches considered
- Trade-offs accepted

### patterns.md
Common patterns and conventions used across the codebase:
- Component patterns
- State management patterns
- Data fetching patterns
- Error handling patterns

### glossary.md
Project-specific terminology and definitions to ensure consistent understanding.

### blockers.md
Current blockers, known issues, and technical debt that need addressing.

## Usage

### For AI Agents
- Read context docs before making architectural decisions
- Update context when new patterns emerge
- Reference decisions when making similar choices
- Keep glossary updated with new terminology

### For Developers
- Consult when wondering "why did we do it this way?"
- Add new entries when making significant decisions
- Update when patterns evolve or change

## Guidelines

1. **Be concise**: Context should be quickly scannable
2. **Date entries**: Include date and author for decisions
3. **Link to code**: Reference specific files or PRs when relevant
4. **Update regularly**: Keep context current with the codebase
5. **Explain rationale**: Focus on "why" not just "what"

---

For coordination between AI agents, see `AGENTS.md` in the root directory.
