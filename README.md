# FileUploads

An AI-Aware React/TypeScript application built with **Spec-Driven Development** principles.

## Overview

This project demonstrates a modern approach to AI-assisted development, where specifications drive implementation and AI agents collaborate effectively through clear contracts and documentation.

### Key Features

- 🤖 **AI-Aware Architecture** - Structured for optimal AI agent collaboration
- 📋 **Spec-Driven Development** - Specifications are the source of truth
- 🔒 **Strict TypeScript** - No `any` types, full type safety
- 🎨 **Tailwind CSS** - Utility-first styling approach
- 🧩 **Modular Components** - Self-contained, reusable views
- 🏗️ **Clean Architecture** - Clear separation of concerns

## Project Structure

```
FileUploads/
├── .github/
│   ├── instructions/          # Agent-specific instructions
│   └── copilot-instructions.md # Strict coding standards
├── docs/
│   ├── specs/                 # Feature specifications (SOURCE OF TRUTH)
│   └── context/               # Project context & decisions
├── src/
│   ├── components/
│   │   └── dynamic/           # Modular, reusable components
│   ├── App.tsx                # Root component
│   └── main.tsx               # Application entry point
├── AGENTS.md                  # AI agent coordination guide
├── GEMINI.md                  # Vision & architectural guidelines
└── package.json               # Dependencies & scripts
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Type check
npm run type-check

# Lint code
npm run lint
```

### Development Workflow

1. **Check Specifications** - Review `/docs/specs/` for feature requirements
2. **Read Context** - Understand patterns in `/docs/context/`
3. **Implement** - Follow strict TypeScript and Tailwind CSS standards
4. **Test** - Verify changes work as expected
5. **Document** - Update specs and context as needed

## AI Agent Collaboration

This repository is optimized for AI-assisted development:

### For Gemini
- See `GEMINI.md` for vision and architectural guidelines
- Focus on specifications, architecture, and code reviews
- Create specs in `/docs/specs/` before implementation

### For GitHub Copilot
- See `.github/copilot-instructions.md` for strict standards
- Implement features based on specifications
- Follow TypeScript strict mode (no `any` types)
- Use Tailwind CSS exclusively for styling

### For All AI Agents
- See `AGENTS.md` for coordination protocol
- Specifications in `/docs/specs/` are the source of truth
- Follow Spec-Driven Development workflow
- Maintain modular, clean architecture

## Core Principles

### 1. Spec-Driven Development
Every feature begins with a specification in `/docs/specs/`. No implementation without a spec.

### 2. Type Safety First
TypeScript strict mode with zero `any` types. Let the compiler catch errors.

### 3. Modular Architecture
Components in `/src/components/dynamic/` are self-contained and composable.

### 4. Utility-First Styling
Tailwind CSS only - no separate CSS files, no inline styles (except dynamic values).

### 5. Accessibility
ARIA labels, semantic HTML, keyboard navigation - built-in from the start.

## Technology Stack

- **React 18** - UI library
- **TypeScript 5** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **ESLint** - Code linting with strict rules

## Documentation

- **[AGENTS.md](./AGENTS.md)** - AI agent coordination guide
- **[GEMINI.md](./GEMINI.md)** - Vision and architectural guidelines
- **[.github/copilot-instructions.md](./.github/copilot-instructions.md)** - Strict coding standards
- **[/docs/specs/](./docs/specs/)** - Feature specifications (source of truth)
- **[/docs/context/](./docs/context/)** - Project context and decisions

## Contributing

This project follows Spec-Driven Development:

1. Create or update specification in `/docs/specs/`
2. Implement according to the spec
3. Follow standards in `.github/copilot-instructions.md`
4. Update context documentation if new patterns emerge

## License

[Add your license here]

---

**Built with AI-Native Development principles** 🤖✨ 
