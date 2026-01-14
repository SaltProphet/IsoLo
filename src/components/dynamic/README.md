# Dynamic Components

This directory contains **modular, reusable view components** that follow strict AI-Aware architecture principles.

## Principles

Every component in this directory must:

1. **Export its props interface** - Enable type-safe usage
2. **Use strict TypeScript** - No `any` types allowed
3. **Style with Tailwind only** - No separate CSS files
4. **Be self-contained** - No hidden dependencies
5. **Have clear documentation** - JSDoc comments for complex logic
6. **Be accessible** - ARIA labels, keyboard navigation, semantic HTML

## Component Structure

```typescript
import React from 'react';

/**
 * Props documentation
 */
export interface ComponentNameProps {
  requiredProp: string;
  optionalProp?: number;
}

/**
 * Component documentation with usage example
 */
export function ComponentName(props: ComponentNameProps): React.JSX.Element {
  // Implementation
}
```

## Current Components

### Card
A versatile card component for displaying content in a contained format.

**Usage:**
```tsx
import { Card } from './components/dynamic/Card';

<Card 
  title="Welcome" 
  description="Get started"
  variant="elevated"
>
  <button>Action</button>
</Card>
```

## Adding New Components

1. Create component file: `ComponentName.tsx`
2. Follow the structure template above
3. Ensure strict TypeScript compliance
4. Add to this README with usage example
5. Reference specification if implementing from spec

## Testing

When tests are added, each component should have:
- Unit tests for logic
- Render tests for output
- Interaction tests for user events
- Accessibility tests for a11y compliance

---

For more patterns and guidelines, see `/docs/context/patterns.md`.
