# GitHub Copilot Strict Coding Standards

These instructions apply to ALL code generation, modification, and suggestions in this repository.

## Fundamental Rules

### 1. TypeScript Strict Mode - MANDATORY
- **NEVER use `any` type** - This is a hard rule with zero exceptions
- Use `unknown` for truly unknown types, then narrow with type guards
- Explicit return types for all exported functions
- Explicit types for all function parameters
- Use `satisfies` operator for type validation without widening

### 2. Type Safety Requirements
```typescript
// ❌ FORBIDDEN
function process(data: any) {
  return data.value;
}

// ✅ REQUIRED
function process(data: unknown): string {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    const record = data as Record<string, unknown>;
    if (typeof record.value === 'string') {
      return record.value;
    }
  }
  throw new Error('Invalid data structure');
}

// ✅ BETTER - Use proper types
interface DataStructure {
  value: string;
}

function process(data: DataStructure): string {
  return data.value;
}
```

### 3. React Component Standards

#### Component Structure
```typescript
// ✅ REQUIRED Format
import React from 'react';

export interface ComponentNameProps {
  requiredProp: string;
  optionalProp?: number;
  onEvent: (data: string) => void;
}

export function ComponentName(props: ComponentNameProps): React.JSX.Element {
  // Implementation
  return <div>{props.requiredProp}</div>;
}
```

#### Component Rules
- **Always** export props interface
- **Always** use explicit return type `React.JSX.Element`
- **Never** use default exports for components (named exports only)
- **Always** destructure props or use `props.` prefix (be consistent in file)
- **Always** use functional components (no class components)

### 4. Tailwind CSS - Required Styling Approach
- **ONLY use Tailwind CSS** for styling
- No inline styles except for dynamic values
- No separate CSS/SCSS files for components (use Tailwind utilities)
- Use Tailwind's responsive prefixes (`sm:`, `md:`, `lg:`, `xl:`)
- Use Tailwind's state variants (`hover:`, `focus:`, `active:`, `disabled:`)

```typescript
// ✅ CORRECT
<button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg disabled:opacity-50">
  Submit
</button>

// ❌ FORBIDDEN
<button style={{ padding: '8px 16px', backgroundColor: 'blue' }}>
  Submit
</button>
```

### 5. Modularity Requirements

#### File Organization
```
src/
├── components/
│   └── dynamic/        # Modular, reusable components ONLY
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Modal.tsx
├── hooks/              # Custom React hooks
├── types/              # Shared TypeScript types
├── utils/              # Pure utility functions
└── services/           # Business logic, API calls
```

#### Component Modularity
- Components in `/components/dynamic/` must be **self-contained**
- Props-driven, no hidden dependencies
- No direct DOM manipulation
- No global state mutations
- Each component focuses on ONE responsibility

### 6. Import Standards
```typescript
// ✅ CORRECT - Organize imports
import React from 'react';                    // 1. React
import { useState, useEffect } from 'react';  // 2. React hooks
                                              // 3. Empty line
import { Button } from './components/dynamic/Button'; // 4. Local imports
import type { User } from './types/user';     // 5. Type imports

// ❌ FORBIDDEN - No relative parent traversal beyond one level
import { something } from '../../../utils/something'; // BAD
```

### 7. Error Handling
```typescript
// ✅ REQUIRED - Explicit error handling
function parseData(input: string): Result {
  try {
    const parsed = JSON.parse(input);
    return { success: true, data: parsed };
  } catch (error) {
    if (error instanceof SyntaxError) {
      return { success: false, error: 'Invalid JSON format' };
    }
    return { success: false, error: 'Unknown error occurred' };
  }
}

// ❌ FORBIDDEN - Swallowing errors
function parseData(input: string) {
  try {
    return JSON.parse(input);
  } catch {
    return null; // BAD: Lost error information
  }
}
```

### 8. Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Components | PascalCase | `FileUploadZone` |
| Functions | camelCase | `formatDate` |
| Constants | UPPER_SNAKE_CASE | `MAX_FILE_SIZE` |
| Interfaces | PascalCase | `UserProfile` |
| Type Aliases | PascalCase | `StatusType` |
| Files (components) | PascalCase | `FileUpload.tsx` |
| Files (utils) | camelCase | `formatDate.ts` |

### 9. Props and State Typing
```typescript
// ✅ REQUIRED - Explicit interface
export interface FormProps {
  initialValue: string;
  onSubmit: (value: string) => void;
  onCancel?: () => void;
}

// ✅ REQUIRED - State typing
const [value, setValue] = useState<string>('');
const [items, setItems] = useState<Item[]>([]);
const [status, setStatus] = useState<'idle' | 'loading' | 'error'>('idle');

// ❌ FORBIDDEN - Implicit any
const [data, setData] = useState(); // BAD
```

### 10. Spec-Driven Development - CRITICAL

**BEFORE implementing ANY feature:**
1. Check if spec exists in `/docs/specs/[feature]-spec.md`
2. If spec doesn't exist, REQUEST spec creation first
3. NEVER implement features without a specification
4. If spec is unclear, REQUEST clarification

**Implementation Process:**
```
1. Read specification → 2. Implement code → 3. Write tests → 4. Update docs
```

### 11. Comments and Documentation

#### When to Comment
```typescript
// ✅ Comment complex business logic
function calculateDiscount(price: number, userLevel: number): number {
  // Apply tiered discount based on user level
  // Level 1: 5%, Level 2: 10%, Level 3: 15%
  const discountRate = Math.min(userLevel * 0.05, 0.15);
  return price * (1 - discountRate);
}

// ❌ Don't comment obvious code
// Set the name variable to userName
const name = userName; // BAD
```

#### JSDoc for Exported Functions
```typescript
/**
 * Validates and formats a phone number
 * @param phone - Raw phone number input
 * @returns Formatted phone number or null if invalid
 */
export function formatPhoneNumber(phone: string): string | null {
  // Implementation
}
```

### 12. Testing Standards (When Tests Exist)
- Write tests alongside implementation
- Test file naming: `ComponentName.test.tsx`
- Test public interface, not implementation details
- Use descriptive test names: `it('should reject files larger than 5MB')`

### 13. Accessibility Requirements
- **ALWAYS** include `alt` text for images
- **ALWAYS** use semantic HTML (`<button>`, `<nav>`, `<main>`, etc.)
- **ALWAYS** include ARIA labels for icon-only buttons
- **ALWAYS** ensure keyboard navigation works
- **ALWAYS** maintain focus management

```typescript
// ✅ REQUIRED
<button
  className="p-2 rounded"
  aria-label="Close dialog"
  onClick={handleClose}
>
  <XIcon className="w-5 h-5" />
</button>

// ❌ FORBIDDEN
<div onClick={handleClose}>X</div>
```

### 14. Performance Considerations
- Use `React.memo()` for expensive components
- Use `useMemo()` for expensive calculations
- Use `useCallback()` for callback props to memoized children
- Lazy load routes and heavy components
- Avoid inline object/array creation in render

```typescript
// ✅ CORRECT
const memoizedValue = useMemo(() => expensiveCalculation(data), [data]);

// ❌ FORBIDDEN - Creates new object every render
<Component config={{ value: 1 }} />

// ✅ CORRECT - Stable reference
const config = useMemo(() => ({ value: 1 }), []);
<Component config={config} />
```

### 15. Git Commit Messages
When implementation involves new code:
```
feat: implement [feature] per spec [spec-name]
fix: resolve [issue] in [component]
refactor: improve [component] structure
docs: update [documentation] for [feature]
test: add tests for [feature]
```

## Enforcement

These standards are **NON-NEGOTIABLE**. Any code generation or suggestion that violates these rules is incorrect and must be revised.

### Checklist for Every Code Change
- [ ] No `any` types used
- [ ] All functions have explicit return types
- [ ] Props interface exported for React components
- [ ] Tailwind CSS used exclusively for styling
- [ ] Component is modular and self-contained
- [ ] Imports are organized correctly
- [ ] Error handling is explicit
- [ ] Naming conventions followed
- [ ] Specification exists and was followed
- [ ] Accessibility requirements met
- [ ] No new ESLint warnings or errors

## Questions?

If you encounter a situation not covered by these standards:
1. Consult `/docs/specs/` for feature-specific guidance
2. Check `/docs/context/` for project patterns
3. Reference `AGENTS.md` for coordination with other agents
4. Default to TypeScript and React best practices

---

**Remember**: These standards exist to maintain code quality, type safety, and AI-readability. Follow them strictly.
