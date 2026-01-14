# AI Agent Coordination Guide

This document defines how AI agents (Gemini, GitHub Copilot, and other AI assistants) should coordinate when working on this codebase.

## Overview

This repository follows **Spec-Driven Development (SDD)**, where specifications in `/docs/specs/` are the **source of truth** for all code generation and modifications. AI agents must consult specifications before making changes.

## Agent Roles

### Gemini
- **Primary Role**: Strategic planning, architecture decisions, and complex problem-solving
- **Responsibilities**:
  - Creating and updating specifications in `/docs/specs/`
  - High-level architecture and design decisions
  - Code reviews and quality assurance
  - Complex refactoring and system-wide changes
- **Reference**: See `GEMINI.md` for detailed vision and guidelines

### GitHub Copilot
- **Primary Role**: Tactical code implementation and inline assistance
- **Responsibilities**:
  - Implementing features based on specifications
  - Writing unit tests and documentation
  - Code completion and suggestions
  - Following strict coding standards
- **Reference**: See `.github/copilot-instructions.md` for strict guidelines

## Coordination Protocol

### 1. Before Making Changes
1. **Check Specifications**: Always review relevant specs in `/docs/specs/`
2. **Check Context**: Review `/docs/context/` for project-specific knowledge
3. **Verify Standards**: Ensure compliance with `.github/copilot-instructions.md`

### 2. Workflow
```
Specification → Implementation → Testing → Documentation
```

1. **Specification Phase** (Gemini-led)
   - Create/update spec in `/docs/specs/[feature-name].md`
   - Define requirements, architecture, and acceptance criteria
   
2. **Implementation Phase** (Copilot-led)
   - Implement code following the specification
   - Write tests for new functionality
   - Update inline documentation

3. **Review Phase** (Gemini-led)
   - Verify implementation matches specification
   - Code quality and architecture review
   - Update context documentation if needed

### 3. Communication Between Agents

- **Handoff Points**: Use comments in specs to indicate completion status
- **Blocking Issues**: Document in `/docs/context/blockers.md`
- **Decisions Log**: Record major decisions in `/docs/context/decisions.md`

## Spec-Driven Development Rules

### For All AI Agents

1. **Specifications are Source of Truth**
   - Never implement features without a specification
   - If spec is unclear, request clarification before proceeding
   - Update spec if requirements change during implementation

2. **Modular Architecture**
   - Keep components small and focused
   - Use `/src/components/dynamic/` for modular, reusable views
   - Follow clean architecture principles

3. **Type Safety First**
   - No `any` types allowed (enforced by TypeScript strict mode)
   - Explicit typing for all function parameters and returns
   - Use type guards for runtime type checking

4. **Testing Requirements**
   - Write tests before or alongside implementation
   - Test coverage for critical paths
   - Integration tests for component interactions

## Directory Structure

```
/docs/
  /specs/          - Feature specifications (SOURCE OF TRUTH)
  /context/        - Project context, decisions, and knowledge
/.github/
  /instructions/   - Agent-specific instructions
  copilot-instructions.md - Copilot strict standards
AGENTS.md          - This file (coordination guide)
GEMINI.md          - Gemini vision and guidelines
```

## File Naming Conventions

- Specifications: `/docs/specs/[feature-name]-spec.md`
- Context docs: `/docs/context/[topic]-context.md`
- Components: PascalCase (e.g., `FileUpload.tsx`)
- Utilities: camelCase (e.g., `formatDate.ts`)

## Version Control

- Commit messages should reference spec when implementing features
- Format: `feat: implement [feature] per spec [spec-name]`
- Breaking changes require spec update FIRST

## Conflict Resolution

If agents disagree on implementation:
1. Default to the specification
2. If spec is ambiguous, Gemini clarifies with spec update
3. Document decision in `/docs/context/decisions.md`

## Getting Started

1. **New Feature**: Create spec in `/docs/specs/` first
2. **Bug Fix**: Check if behavior matches spec; update spec if needed
3. **Refactoring**: Ensure no breaking changes to spec contracts

---

**Remember**: Specifications drive development. When in doubt, consult the spec or create one.
