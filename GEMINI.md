# Gemini Vision & Guidelines

## Vision

This project represents an **AI-Native Development** approach where AI agents work collaboratively to build high-quality, maintainable software. The FileUploads application serves as a foundation for demonstrating Spec-Driven Development (SDD) principles with React and TypeScript.

## Core Philosophy

### 1. Specification-Driven Excellence
Every feature begins with a clear specification. Code is an implementation detail; the spec defines the contract.

### 2. Type Safety as Foundation
TypeScript's strict mode isn't a restriction—it's a design tool that catches errors at compile time and improves code clarity.

### 3. Modular, Composable Architecture
Build small, focused components that compose into larger systems. Each component should have a single, well-defined purpose.

### 4. AI-Augmented, Human-Centric
AI accelerates development, but the architecture must remain understandable to human developers.

## Architectural Vision

### Component Architecture

```
src/
├── components/
│   ├── dynamic/          # Modular, reusable view components
│   │   ├── FileUploadZone.tsx
│   │   ├── FilePreview.tsx
│   │   └── ProgressIndicator.tsx
│   ├── layouts/          # Layout components
│   └── common/           # Shared UI components
├── hooks/                # Custom React hooks
├── services/             # Business logic and API calls
├── types/                # TypeScript type definitions
├── utils/                # Utility functions
└── App.tsx               # Root component
```

### Design Principles

#### 1. Progressive Disclosure
Start with simple interfaces, reveal complexity only when needed.

#### 2. Composition Over Configuration
Prefer composing small components over complex configuration objects.

#### 3. Explicit Over Implicit
Make dependencies and data flow explicit. No hidden state or magic.

#### 4. Fail Fast
Type errors at compile time are better than runtime errors. Use TypeScript's type system fully.

## Development Workflow

### Phase 1: Specification
**Gemini's Primary Responsibility**

1. **Understand Requirements**: Clarify user needs and business goals
2. **Define Architecture**: Design component structure and data flow
3. **Write Specification**: Create detailed spec in `/docs/specs/`
4. **Set Acceptance Criteria**: Define what "done" looks like

**Spec Template**:
```markdown
# [Feature Name] Specification

## Purpose
[Why this feature exists]

## Requirements
- Functional requirements
- Non-functional requirements (performance, accessibility, etc.)

## Architecture
- Component structure
- Data flow
- State management

## API Contracts
- Props interfaces
- Function signatures
- Event handlers

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Testing Strategy
[How to verify the implementation]
```

### Phase 2: Implementation
**Copilot's Primary Responsibility** (with Gemini oversight)

1. **Read Specification**: Understand requirements fully
2. **Implement Features**: Write code following strict standards
3. **Write Tests**: Ensure code meets acceptance criteria
4. **Document Code**: Add inline docs for complex logic

### Phase 3: Review & Refinement
**Gemini's Primary Responsibility**

1. **Verify Against Spec**: Ensure implementation matches requirements
2. **Code Quality Review**: Check for maintainability and best practices
3. **Performance Review**: Identify potential bottlenecks
4. **Update Context**: Document learnings in `/docs/context/`

## Quality Standards

### TypeScript
- **Strict mode enabled**: No escape hatches
- **No `any` types**: Use `unknown` or proper types
- **Explicit return types**: For all exported functions
- **Type guards**: For runtime type validation

### React
- **Functional components**: No class components
- **Hooks for logic**: Custom hooks for reusable logic
- **Props interfaces**: Explicitly typed, exported
- **Component composition**: Small, focused components

### Styling
- **Tailwind CSS**: Utility-first approach
- **Responsive design**: Mobile-first breakpoints
- **Accessibility**: ARIA labels, keyboard navigation
- **Consistent spacing**: Use Tailwind's spacing scale

### Testing (Future)
- **Unit tests**: For utilities and hooks
- **Component tests**: For UI components
- **Integration tests**: For feature flows
- **Type tests**: Verify type contracts

## File Organization

### Modular Components (`/src/components/dynamic/`)
This directory contains **reusable, modular view components** that can be composed together.

**Characteristics**:
- Self-contained with clear interfaces
- Props-driven, no hidden dependencies
- Fully typed with exported interfaces
- Documented with JSDoc comments
- Example implementations included

**Example Structure**:
```typescript
// FileUploadZone.tsx
export interface FileUploadZoneProps {
  onFilesSelected: (files: File[]) => void;
  acceptedTypes?: string[];
  maxSize?: number;
  multiple?: boolean;
}

export function FileUploadZone(props: FileUploadZoneProps): React.JSX.Element {
  // Implementation
}
```

### Documentation Structure

#### `/docs/specs/`
The **source of truth** for all features. Every feature must have a spec before implementation.

#### `/docs/context/`
Project knowledge that helps AI agents understand:
- **decisions.md**: Major architectural decisions and rationale
- **patterns.md**: Common patterns used in the codebase
- **blockers.md**: Known issues and blockers
- **glossary.md**: Project-specific terminology

## AI Agent Expectations

### What Gemini Should Do
- ✅ Strategic planning and architecture
- ✅ Writing and updating specifications
- ✅ High-level code reviews
- ✅ Resolving ambiguities
- ✅ Making architectural decisions
- ✅ Updating context documentation

### What Gemini Should NOT Do
- ❌ Implement features without writing a spec first
- ❌ Make tactical code changes (that's Copilot's role)
- ❌ Override TypeScript strict mode
- ❌ Add complexity without justification

### Collaboration Model
- **Gemini**: Sets direction, defines contracts, ensures quality
- **Copilot**: Implements features, writes tests, follows standards
- **Handoff**: Via specifications and clear documentation

## Success Metrics

### Code Quality
- Zero TypeScript errors or warnings
- No `any` types in codebase
- Consistent code style (enforced by linting)
- Clear component boundaries

### Maintainability
- Every feature has a specification
- Components are small and focused
- Dependencies are explicit
- Code is self-documenting

### AI Effectiveness
- Specs enable autonomous implementation
- Context docs reduce repeated questions
- Clear standards minimize back-and-forth
- Modular structure enables parallel work

## Future Enhancements

### Planned Additions
1. **Testing Framework**: Jest + React Testing Library
2. **State Management**: Context API or Zustand for complex state
3. **Form Validation**: Zod or Yup for schema validation
4. **API Integration**: Axios + React Query for server communication
5. **Error Boundaries**: Graceful error handling
6. **Performance Monitoring**: React DevTools + Web Vitals

### Architecture Evolution
- Component library documentation
- Storybook for component showcase
- E2E testing with Playwright
- CI/CD pipeline configuration
- Accessibility testing automation

---

**Remember**: This is a living document. Update it as the project evolves and new patterns emerge.
