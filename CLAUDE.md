# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

### Frontend (Next.js)
```bash
cd frontend
npm run dev          # Start development server with Turbopack
npm run build        # Build for production
npm run lint         # Run ESLint
npm run format       # Format code with Prettier
npm run format:check # Check code formatting
```

### Backend (Python/FastAPI)
```bash
cd backend
uv run python api.py          # Start FastAPI development server
uv run pytest               # Run tests
uv run pytest path/to/test.py # Run specific test
```

### Full Stack Development
```bash
# Start both frontend and backend locally
docker-compose up  # Runs both services with dependencies
```

## Architecture Overview

### Full-Stack AI Worker Platform
Suna is a generalist AI Worker platform with three main components:

1. **Frontend**: Next.js 15+ dashboard for agent management, chat interfaces, workflow builders
2. **Backend**: Python/FastAPI service with agent orchestration, tool execution, LLM integration
3. **Agent Runtime**: Docker-isolated environments for safe agent execution

### Key Architectural Patterns

#### Backend (Python/FastAPI)
- **Tool System**: Dual schema decorators (`@openapi_schema`) for OpenAPI + XML tool definitions
- **Agent Builder Tools**: Extend `AgentBuilderBaseTool` for agent configuration tools
- **Thread Management**: `ThreadManager` handles conversation context and agent execution
- **Background Jobs**: Dramatiq workers for async processing
- **Authentication**: JWT validation with Supabase (no signature verification required)
- **Database**: Supabase PostgreSQL with Row Level Security (RLS)

#### Frontend (Next.js/React)
- **UI Framework**: shadcn/ui components with Radix UI primitives
- **State Management**: React Query for server state, React hooks for local state
- **Forms**: React Hook Form with Zod validation
- **Authentication**: Supabase Auth with automatic token management
- **Real-time**: Supabase subscriptions for live updates

#### Agent System
- **Versioning**: Multiple agent versions tracked in `agent_versions` table
- **Configuration**: JSONB config storage with validation schemas
- **Workflows**: Multi-step execution defined in `agent_workflows`
- **Tools**: Modular tool system with runtime registration
- **Triggers**: Scheduled and event-based agent automation

### Database Schema Patterns
- UUID primary keys with `gen_random_uuid()`
- Automatic `created_at`/`updated_at` timestamps via triggers
- Foreign key relationships with CASCADE deletes
- Row Level Security policies for multi-tenant access
- JSONB columns for flexible configuration storage

### Tool Development Framework
```python
# Standard tool pattern
class ExampleTool(AgentBuilderBaseTool):
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "tool_name",
            "description": "Clear description of what the tool does",
            "parameters": {
                "type": "object",
                "properties": {
                    "param": {"type": "string", "description": "Parameter description"}
                },
                "required": ["param"]
            }
        }
    })
    async def tool_name(self, param: str) -> ToolResult:
        # Implementation with proper error handling
        return self.success_response(result=data, message="Success message")
```

### Frontend Component Patterns
- Use shadcn/ui components as default UI building blocks
- React Query hooks in `src/hooks/react-query/` for data fetching
- Context providers for global state (auth, billing, etc.)
- File-based routing with App Router
- TypeScript interfaces for all data structures

### Configuration Management
- Environment-specific configs via `utils.config.EnvMode`
- Feature flags via `flags.flags.is_enabled()`
- Secure credential storage with Fernet encryption
- Supabase client configuration for frontend/backend

### Testing Approach
- **Backend**: pytest with async support for unit and integration tests
- **Frontend**: Component testing patterns with React Testing Library
- **Integration**: API endpoint testing with real database
- **E2E**: Critical user flow validation

### Security Considerations
- All database access through RLS policies
- Credential encryption for sensitive data
- Input validation via Pydantic models
- Rate limiting and timeout enforcement
- Sandbox isolation for agent execution

## Important File Locations

- `backend/agent/run.py` - Core agent execution engine
- `backend/tools/` - Agent tool implementations
- `frontend/src/components/agents/` - Agent management UI
- `backend/supabase/migrations/` - Database schema definitions
- `.cursor/rules/` - Development guidelines for different components