# Common Patterns

This document describes common patterns and conventions used throughout the FileUploads codebase.

## Component Patterns

### 1. Props Interface Pattern
Always export the props interface for components:

```typescript
export interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: 'primary' | 'secondary';
  disabled?: boolean;
}

export function Button(props: ButtonProps): React.JSX.Element {
  // Implementation
}
```

### 2. Conditional Rendering Pattern
Use explicit conditionals for clarity:

```typescript
// ✅ Preferred - Clear intent
{isLoading ? <Spinner /> : <Content data={data} />}

// ✅ Also good - Guard clause
{!data && <EmptyState />}
{data && <Content data={data} />}

// ❌ Avoid - Can cause issues with numbers/strings
{count && <Badge count={count} />}  // Shows "0" if count is 0

// ✅ Correct
{count > 0 && <Badge count={count} />}
```

### 3. Event Handler Pattern
Type event handlers explicitly:

```typescript
interface FormProps {
  onSubmit: (data: FormData) => void;
}

function Form(props: FormProps): React.JSX.Element {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault();
    // Process form
    props.onSubmit(formData);
  };

  return <form onSubmit={handleSubmit}>...</form>;
}
```

### 4. Custom Hook Pattern
Extract reusable logic into custom hooks:

```typescript
export function useFileUpload() {
  const [files, setFiles] = useState<File[]>([]);
  const [uploading, setUploading] = useState(false);

  const upload = async (file: File): Promise<void> => {
    setUploading(true);
    try {
      // Upload logic
    } finally {
      setUploading(false);
    }
  };

  return { files, uploading, upload };
}
```

## State Management Patterns

### 1. Local State
Use `useState` for component-specific state:

```typescript
const [isOpen, setIsOpen] = useState(false);
const [items, setItems] = useState<Item[]>([]);
```

### 2. Derived State
Use `useMemo` for computed values:

```typescript
const totalPrice = useMemo(() => {
  return items.reduce((sum, item) => sum + item.price, 0);
}, [items]);
```

### 3. Complex State
Use `useReducer` for state with multiple sub-values:

```typescript
interface State {
  loading: boolean;
  error: string | null;
  data: Data | null;
}

type Action =
  | { type: 'LOADING' }
  | { type: 'SUCCESS'; payload: Data }
  | { type: 'ERROR'; payload: string };

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case 'LOADING':
      return { ...state, loading: true, error: null };
    case 'SUCCESS':
      return { loading: false, error: null, data: action.payload };
    case 'ERROR':
      return { loading: false, error: action.payload, data: null };
  }
}
```

## Error Handling Patterns

### 1. Result Type Pattern
Return result objects instead of throwing:

```typescript
type Result<T, E = string> =
  | { success: true; data: T }
  | { success: false; error: E };

function parseJSON<T>(text: string): Result<T> {
  try {
    return { success: true, data: JSON.parse(text) };
  } catch (error) {
    return { success: false, error: 'Invalid JSON' };
  }
}

// Usage
const result = parseJSON<User>(response);
if (result.success) {
  console.log(result.data); // TypeScript knows this is User
} else {
  console.error(result.error);
}
```

### 2. Error Boundary Pattern
Wrap components that might error:

```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError(): { hasError: boolean } {
    return { hasError: true };
  }

  render(): React.ReactNode {
    if (this.state.hasError) {
      return <ErrorFallback />;
    }
    return this.props.children;
  }
}
```

## Data Fetching Patterns

### 1. Async Effect Pattern
Fetch data in `useEffect`:

```typescript
function UserProfile({ userId }: { userId: string }): React.JSX.Element {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function fetchUser(): Promise<void> {
      try {
        const data = await api.getUser(userId);
        if (!cancelled) {
          setUser(data);
        }
      } catch (err) {
        if (!cancelled) {
          setError(err instanceof Error ? err.message : 'Unknown error');
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchUser();

    return () => {
      cancelled = true;
    };
  }, [userId]);

  if (loading) return <Spinner />;
  if (error) return <Error message={error} />;
  if (!user) return <NotFound />;
  return <UserCard user={user} />;
}
```

## Type Patterns

### 1. Union Types for State
Use discriminated unions:

```typescript
type LoadingState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: string };

// TypeScript narrows the type
if (state.status === 'success') {
  console.log(state.data); // TypeScript knows data exists
}
```

### 2. Type Guards
Create type guards for runtime checks:

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

// Usage
if (isUser(data)) {
  console.log(data.name); // TypeScript knows this is User
}
```

### 3. Const Assertions
Use `as const` for literal types:

```typescript
const STATUSES = ['idle', 'loading', 'success', 'error'] as const;
type Status = typeof STATUSES[number]; // 'idle' | 'loading' | 'success' | 'error'
```

## File Organization Pattern

```
ComponentName/
├── ComponentName.tsx       # Main component
├── ComponentName.test.tsx  # Tests (when added)
├── types.ts                # Component-specific types
└── utils.ts                # Component-specific utilities
```

For simple components, keep everything in one file:
```
ComponentName.tsx  # Component + types + utils
```

## Styling Patterns

### 1. Responsive Design
```typescript
<div className="flex flex-col md:flex-row gap-4">
  {/* Mobile: vertical, Desktop: horizontal */}
</div>
```

### 2. Conditional Classes
```typescript
const buttonClasses = `
  px-4 py-2 rounded
  ${variant === 'primary' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800'}
  ${disabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80'}
`;
```

### 3. Common Spacing
Use Tailwind's spacing scale consistently:
- `gap-4`, `p-4`, `m-4` for normal spacing
- `gap-2`, `p-2`, `m-2` for tight spacing
- `gap-8`, `p-8`, `m-8` for loose spacing

---

*Update this document as new patterns emerge in the codebase.*
