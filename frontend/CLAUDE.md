# CLAUDE.md - Frontend

This file provides guidance to Claude Code (claude.ai/code) when working with the frontend code in this repository.

## Development Commands

```bash
npm run dev          # Start development server with Turbopack
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check code formatting
```

## Frontend Architecture

### Tech Stack
- **Framework**: Next.js 15+ with App Router and Turbopack
- **Language**: TypeScript 5+ with strict type checking
- **Styling**: Tailwind CSS 4+ with shadcn/ui components
- **State Management**: React Query + Zustand stores
- **Authentication**: Supabase Auth with automatic token management
- **UI Library**: Radix UI primitives via shadcn/ui

### Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── (dashboard)/       # Dashboard routes with shared layout
│   ├── (home)/           # Marketing/landing pages
│   ├── api/              # API routes and webhooks
│   └── auth/             # Authentication pages
├── components/            # Reusable components organized by feature
│   ├── agents/           # Agent management components
│   ├── thread/           # Chat interface components
│   ├── ui/               # shadcn/ui base components
│   └── billing/          # Billing and subscription components
├── hooks/                # Custom React hooks
│   └── react-query/      # Data fetching hooks organized by domain
├── lib/                  # Utilities and configurations
│   ├── api.ts           # API client with error handling
│   ├── supabase/        # Supabase client configuration
│   └── stores/          # Zustand state stores
└── providers/            # Context providers
```

## Key Patterns & Components

### Data Fetching with React Query

All API calls use React Query hooks organized by domain:

```typescript
// Pattern: src/hooks/react-query/[domain]/use-[resource].ts
import { createQueryHook, createMutationHook } from '@/hooks/use-query';
import { agentKeys } from './keys';

export const useAgents = (params: AgentsParams = {}) => {
  return createQueryHook(
    agentKeys.list(params),
    () => getAgents(params),
    {
      staleTime: 5 * 60 * 1000,
      gcTime: 10 * 60 * 1000,
    }
  )();
};

export const useCreateAgent = () => {
  const queryClient = useQueryClient();
  
  return createMutationHook(createAgent, {
    onSuccess: (data) => {
      queryClient.invalidateQueries({ queryKey: agentKeys.lists() });
      toast.success('Agent created successfully');
    },
  })();
};
```

### Component Architecture

#### shadcn/ui Integration
Use shadcn/ui components as the foundation for all UI:

```typescript
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";

// Custom components extend shadcn/ui
const AgentCard = ({ agent }: { agent: Agent }) => (
  <Card className="hover:shadow-md transition-shadow">
    <CardHeader>
      <CardTitle>{agent.name}</CardTitle>
    </CardHeader>
    <CardContent>
      <Button onClick={() => runAgent(agent.id)}>
        Run Agent
      </Button>
    </CardContent>
  </Card>
);
```

#### Form Handling Pattern
```typescript
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormField, FormItem, FormLabel, FormControl } from "@/components/ui/form";

const AgentForm = () => {
  const form = useForm({
    resolver: zodResolver(agentSchema),
    defaultValues: { name: "", description: "" }
  });

  return (
    <Form {...form}>
      <FormField
        control={form.control}
        name="name"
        render={({ field }) => (
          <FormItem>
            <FormLabel>Agent Name</FormLabel>
            <FormControl>
              <Input placeholder="Enter agent name" {...field} />
            </FormControl>
          </FormItem>
        )}
      />
    </Form>
  );
};
```

### Authentication & User Management

#### Supabase Auth Integration
```typescript
// Client-side auth context
import { createClient } from '@/lib/supabase/client';

const supabase = createClient();

// Auth state management
const { data: { user } } = await supabase.auth.getUser();
```

#### Protected Routes
```typescript
// Layout pattern for protected routes
export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen">
      <SidebarLeft />
      <main className="flex-1">{children}</main>
    </div>
  );
}
```

### Real-time Features

#### Supabase Subscriptions
```typescript
// Real-time data updates
useEffect(() => {
  const subscription = supabase
    .channel('agent_updates')
    .on('postgres_changes', 
      { event: 'UPDATE', schema: 'public', table: 'agents' },
      (payload) => {
        queryClient.invalidateQueries({ queryKey: agentKeys.lists() });
      }
    )
    .subscribe();

  return () => subscription.unsubscribe();
}, []);
```

### Chat Interface Architecture

#### Thread Management
- `src/components/thread/content/ThreadContent.tsx` - Main chat interface
- `src/components/thread/chat-input/chat-input.tsx` - Message input with file uploads
- `src/components/thread/tool-views/` - Tool execution result renderers

#### Streaming Responses
```typescript
// Agent streaming with EventSource
const useAgentStream = (threadId: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  
  useEffect(() => {
    const eventSource = new EventSource(`/api/stream/${threadId}`);
    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages(prev => [...prev, data]);
    };
    
    return () => eventSource.close();
  }, [threadId]);
  
  return { messages };
};
```

## State Management Patterns

### Zustand Stores
Global state for UI-specific concerns:

```typescript
// src/lib/stores/agent-selection-store.ts
import { create } from 'zustand';

interface AgentSelectionStore {
  selectedAgentId: string | null;
  setSelectedAgentId: (id: string | null) => void;
}

export const useAgentSelection = create<AgentSelectionStore>((set) => ({
  selectedAgentId: null,
  setSelectedAgentId: (id) => set({ selectedAgentId: id }),
}));
```

### React Query Cache Management
```typescript
// Query key patterns
export const agentKeys = {
  all: ['agents'] as const,
  lists: () => [...agentKeys.all, 'list'] as const,
  list: (params: AgentsParams) => [...agentKeys.lists(), params] as const,
  details: () => [...agentKeys.all, 'detail'] as const,
  detail: (id: string) => [...agentKeys.details(), id] as const,
};
```

## File & Asset Management

### File Upload Handling
```typescript
// File upload with progress tracking
const handleFileUpload = async (files: File[]) => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  
  return await api.post('/files/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (progressEvent) => {
      const progress = Math.round(
        (progressEvent.loaded * 100) / progressEvent.total
      );
      setUploadProgress(progress);
    },
  });
};
```

### Image Rendering
- `src/components/file-renderers/` - Specialized renderers for different file types
- `src/components/thread/preview-renderers/` - Preview components for chat attachments

## Error Handling

### API Error Handling
```typescript
// Custom error classes in src/lib/api.ts
export class BillingError extends Error {
  status: number;
  detail: { message: string; [key: string]: any };
}

export class AgentRunLimitError extends Error {
  status: number;
  detail: { 
    message: string;
    running_thread_ids: string[];
    running_count: number;
  };
}
```

### Error Boundaries
```typescript
// Component-level error handling
const AgentComponent = () => {
  const { data: agents, error, isLoading } = useAgents();
  
  if (error) {
    return <ErrorState error={error} onRetry={() => refetch()} />;
  }
  
  if (isLoading) {
    return <LoadingSkeleton />;
  }
  
  return <AgentsGrid agents={agents} />;
};
```

## Performance Patterns

### Code Splitting
```typescript
// Dynamic imports for heavy components
const AgentBuilder = lazy(() => import('@/components/agents/agent-builder'));

// In component
<Suspense fallback={<LoadingSkeleton />}>
  <AgentBuilder />
</Suspense>
```

### Optimization Hooks
```typescript
// Memoization patterns
const expensiveValue = useMemo(() => 
  computeExpensiveValue(data), [data]
);

const stableCallback = useCallback((id: string) => 
  handleAgentSelect(id), [handleAgentSelect]
);
```

## Key Integrations

### Billing & Subscriptions
- `src/components/billing/` - Stripe integration for subscription management
- `src/hooks/react-query/subscriptions/` - Billing status hooks

### Analytics & Monitoring
- PostHog for user analytics and feature flags
- Vercel Analytics for performance monitoring
- Error tracking via toast notifications

### Composio Integration
- `src/components/agents/composio/` - Third-party tool integration UI
- `src/hooks/react-query/composio/` - Composio API hooks

## Development Guidelines

### TypeScript Best Practices
- Use strict type checking with no `any` types
- Define interfaces for all component props
- Use type imports: `import type { Agent } from '@/types'`
- Leverage utility types: `Partial<T>`, `Pick<T, K>`, `Omit<T, K>`

### Component Guidelines
- Use forwardRef for components that need DOM refs
- Implement proper loading and error states
- Use compound component patterns for complex UI
- Keep components focused on single responsibilities

### Styling Conventions
- Use Tailwind CSS utility classes
- Follow shadcn/ui design system patterns
- Use CSS variables for theme customization
- Implement responsive design with mobile-first approach

### File Organization
- Group related components in feature folders
- Keep reusable UI components in `src/components/ui/`
- Organize hooks by domain in `src/hooks/react-query/`
- Use index files for clean imports