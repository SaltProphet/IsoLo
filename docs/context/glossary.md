# Project Glossary

This document defines project-specific terminology to ensure consistent understanding across the codebase and documentation.

## Terms

### AI-Aware Structure
An application architecture designed to facilitate AI-assisted development. Includes clear specifications, strong type contracts, and modular components that AI agents can understand and generate.

### Spec-Driven Development (SDD)
A development methodology where specifications in `/docs/specs/` serve as the source of truth. All features must have a specification before implementation begins.

### Dynamic Components
Self-contained, reusable UI components in `/src/components/dynamic/`. They are:
- Props-driven with explicit interfaces
- Free of hidden dependencies
- Focused on a single responsibility
- Composable into larger features

### Clean Architecture
Architectural pattern that separates concerns into layers:
- **Presentation**: UI components (React)
- **Domain**: Business logic and rules
- **Data**: API calls and data persistence

### Type Safety
The practice of using TypeScript's type system to catch errors at compile time. In this project, we enforce strict mode with zero `any` types.

### Modular Views
UI components designed to be independently developed, tested, and composed. Located in `/src/components/dynamic/`.

### Source of Truth
The authoritative reference for system behavior. In this project, specifications in `/docs/specs/` are the source of truth.

## Component Types

### Layout Component
Components that define page structure (header, sidebar, main content area). Found in `/src/components/layouts/`.

### Common Component
Shared UI primitives (buttons, inputs, modals). Found in `/src/components/common/`.

### Dynamic Component
Modular, feature-specific components. Found in `/src/components/dynamic/`.

## Development Terms

### Agent
An AI assistant (Gemini, GitHub Copilot) that helps with development. See `AGENTS.md` for coordination details.

### Contract
An interface or type definition that establishes how components interact. Includes props, return types, and event signatures.

### Acceptance Criteria
Measurable conditions that must be met for a feature to be considered complete. Defined in specifications.

### Type Guard
A TypeScript function that narrows types at runtime, enabling safe access to properties.

### Utility-First CSS
Styling approach (Tailwind CSS) where pre-defined utility classes are composed to create designs, rather than writing custom CSS.

## File Types

### `.tsx`
TypeScript file with JSX (React components).

### `.ts`
TypeScript file without JSX (utilities, types, services).

### `*-spec.md`
Feature specification document in `/docs/specs/`.

### `*-context.md`
Context documentation in `/docs/context/`.

## Acronyms

- **SDD**: Spec-Driven Development
- **TS**: TypeScript
- **JSX**: JavaScript XML (React's syntax extension)
- **HMR**: Hot Module Replacement
- **SPA**: Single Page Application
- **SSR**: Server-Side Rendering (not used in this project)
- **ARIA**: Accessible Rich Internet Applications
- **WCAG**: Web Content Accessibility Guidelines

## Anti-Patterns to Avoid

### Magic Values
Hardcoded values without explanation. Use named constants instead:
```typescript
// ❌ Magic value
if (status === 3) { ... }

// ✅ Named constant
const STATUS_COMPLETED = 3;
if (status === STATUS_COMPLETED) { ... }
```

### Implicit Any
TypeScript inferring `any` type. Always provide explicit types:
```typescript
// ❌ Implicit any
function process(data) { ... }

// ✅ Explicit type
function process(data: UserData) { ... }
```

### Prop Drilling
Passing props through multiple component layers. Use composition or context instead.

### God Component
A component that does too much. Break into smaller, focused components.

---

*Add new terms as they become important to the project.*
