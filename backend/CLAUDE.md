# CLAUDE.md - Backend

This file provides guidance to Claude Code (claude.ai/code) when working with the backend code in this repository.

## Development Commands

```bash
# Start development server
uv run python api.py

# Run tests
uv run pytest
uv run pytest path/to/test.py  # Run specific test

# Install dependencies
uv sync

# Database operations (via Supabase CLI if available)
supabase db reset
supabase db push
```

## Backend Architecture

### Tech Stack
- **Framework**: FastAPI 0.115+ with async/await patterns
- **Language**: Python 3.11+ with comprehensive type hints
- **Database**: Supabase PostgreSQL with Row Level Security
- **Cache**: Redis 5.2+ for session and data caching
- **LLM Integration**: LiteLLM 1.75+ for multi-provider support
- **Background Jobs**: Dramatiq 1.18+ with Redis broker
- **Monitoring**: Langfuse tracing, Sentry error tracking, Prometheus metrics

### Project Structure

```
backend/
├── api.py                 # Main FastAPI application entry point
├── agent/                 # Core agent system
│   ├── run.py            # Agent execution engine
│   ├── prompt.py         # System prompt templates
│   ├── tools/            # Agent tool implementations
│   │   ├── agent_builder_tools/  # Tools for building/configuring agents
│   │   ├── data_providers/       # External data source tools
│   │   └── sb_*.py              # Sandbox integration tools
│   └── suna/             # Suna-specific agent configurations
├── agentpress/           # Agent framework core
│   ├── thread_manager.py # Conversation management
│   ├── tool_registry.py  # Tool registration system
│   └── response_processor.py # LLM response handling
├── services/             # Business logic services
│   ├── supabase.py      # Database connection management
│   ├── llm.py           # LLM integration layer
│   ├── billing.py       # Stripe billing integration
│   └── redis.py         # Redis cache management
├── utils/                # Shared utilities
│   ├── config.py        # Environment configuration
│   ├── auth_utils.py    # JWT validation and user management
│   ├── logger.py        # Structured logging setup
│   └── encryption.py    # Credential encryption utilities
└── supabase/            # Database schema and migrations
    └── migrations/      # SQL migration files
```

## Core Architectural Patterns

### Tool Development Framework

#### Base Tool Classes
```python
from agent.tools.agent_builder_tools.base_tool import AgentBuilderBaseTool
from agentpress.tool import Tool, openapi_schema, ToolResult

class ExampleTool(AgentBuilderBaseTool):
    @openapi_schema({
        "type": "function",
        "function": {
            "name": "example_action",
            "description": "Detailed description of what this tool does",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {
                        "type": "string",
                        "description": "Clear parameter description"
                    }
                },
                "required": ["param1"]
            }
        }
    })
    async def example_action(self, param1: str) -> ToolResult:
        try:
            # Implementation logic
            result = await self.perform_action(param1)
            
            return self.success_response(
                result=result,
                message=f"Successfully completed action for {param1}"
            )
        except Exception as e:
            logger.error(f"Tool execution failed: {e}", exc_info=True)
            return self.fail_response(f"Failed to perform action: {str(e)}")
```

#### Tool Registration
- Tools extend `AgentBuilderBaseTool` for agent configuration tools
- Tools extend `Tool` for general agent execution tools
- Use `@openapi_schema` decorator for automatic schema generation
- Return `ToolResult` objects with consistent success/failure patterns

### Thread Management System

#### ThreadManager Core
```python
# agent/run.py usage pattern
from agentpress.thread_manager import ThreadManager

async def run_agent(config: AgentConfig):
    thread_manager = ThreadManager(
        trace=langfuse_trace,
        is_agent_builder=False,
        agent_config=agent_config
    )
    
    # Register tools
    await thread_manager.register_tool(MessageTool())
    await thread_manager.register_tool(SandboxShellTool())
    
    # Execute conversation
    async for response in thread_manager.process_messages(
        user_message=message,
        system_prompt=system_prompt,
        model_name=config.model_name
    ):
        yield response
```

#### Message Handling
- Messages stored in `agentpress_messages` table with JSONB content
- Support for text, images, and tool calls
- Automatic token counting and context management
- Streaming responses via AsyncGenerator patterns

### Database Integration Patterns

#### Supabase Connection Management
```python
from services.supabase import DBConnection

# Singleton pattern with async initialization
db = DBConnection()
await db.initialize()
client = await db.client

# Query pattern with error handling
result = await client.table('agents').select('*').eq('agent_id', agent_id).execute()
if not result.data:
    raise ValueError(f"Agent not found: {agent_id}")
```

#### Migration Patterns
All migrations in `backend/supabase/migrations/` follow this structure:
```sql
-- Idempotent migration pattern
BEGIN;

-- Create table with proper constraints
CREATE TABLE IF NOT EXISTS example_table (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES basejump.accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS
ALTER TABLE example_table ENABLE ROW LEVEL SECURITY;

-- Create RLS policy
CREATE POLICY "Account members can access their records" ON example_table
    FOR ALL USING (
        account_id = ANY(basejump.get_account_ids_for_current_user())
    );

COMMIT;
```

### Authentication & Security

#### JWT Validation
```python
# utils/auth_utils.py pattern
from fastapi import Depends, HTTPException
import jwt

async def get_current_user(authorization: str = Header(None)) -> UserClaims:
    """Extract and validate user from JWT token (Supabase format)."""
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    token = authorization.split(' ')[1]
    
    try:
        # Supabase tokens don't require signature verification for internal use
        payload = jwt.decode(token, options={"verify_signature": False})
        return UserClaims(**payload)
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### Credential Encryption
```python
# utils/encryption.py usage
from cryptography.fernet import Fernet

def encrypt_credentials(data: dict) -> str:
    """Encrypt sensitive credential data."""
    key = config.ENCRYPTION_KEY.encode()
    cipher = Fernet(key)
    json_data = json.dumps(data)
    return cipher.encrypt(json_data.encode()).decode()
```

### LLM Integration Layer

#### LiteLLM Configuration
```python
# services/llm.py pattern
import litellm
from utils.config import config

async def make_llm_api_call(
    model: str,
    messages: List[dict],
    tools: Optional[List[dict]] = None,
    stream: bool = False
):
    """Unified LLM API call with provider abstraction."""
    try:
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            tools=tools,
            stream=stream,
            temperature=0.1,
            max_tokens=4096
        )
        return response
    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        raise
```

#### Agent Execution Flow
1. **Configuration**: Load agent config from `agents` table
2. **Tool Registration**: Register tools based on agent configuration
3. **Context Management**: Build system prompt with agent instructions
4. **Execution**: Process user message through LLM with tool support
5. **Tool Execution**: Execute tools in sandbox environments
6. **Response Processing**: Stream results back to frontend

### Background Job System

#### Dramatiq Workers
```python
import dramatiq
from dramatiq.brokers.redis import RedisBroker

# Configure Redis broker
redis_broker = RedisBroker(host=config.REDIS_HOST)
dramatiq.set_broker(redis_broker)

@dramatiq.actor(max_retries=3, min_backoff=1000)
async def process_agent_task(agent_id: str, task_data: dict):
    """Background agent task processing."""
    try:
        # Task implementation
        result = await execute_agent_task(agent_id, task_data)
        return result
    except Exception as e:
        logger.error(f"Background task failed: {e}")
        raise
```

### API Design Patterns

#### FastAPI Route Organization
```python
# api.py main application
from fastapi import FastAPI, APIRouter
from agent import api as agent_api
from triggers import api as triggers_api

app = FastAPI()

# Mount API routers
app.include_router(agent_api.router, prefix="/api/agent", tags=["agent"])
app.include_router(triggers_api.router, prefix="/api/triggers", tags=["triggers"])
```

#### Request/Response Models
```python
from pydantic import BaseModel, Field
from typing import Optional, List

class AgentCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    model_name: str = "claude-3-5-sonnet-20241022"

class AgentResponse(BaseModel):
    agent_id: str
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
```

### Sandbox Integration

#### Tool Execution Pattern
```python
# tools/sb_*.py pattern for sandbox tools
class SandboxShellTool(Tool):
    async def execute_command(self, command: str) -> ToolResult:
        """Execute shell command in isolated sandbox."""
        try:
            # Sandbox API call
            response = await self.sandbox_client.execute(command)
            
            return self.success_response(
                result=response.output,
                message="Command executed successfully"
            )
        except Exception as e:
            return self.fail_response(f"Command execution failed: {str(e)}")
```

### Configuration Management

#### Environment Configuration
```python
# utils/config.py usage
from utils.config import config, EnvMode

# Access configuration values
if config.ENV_MODE == EnvMode.PRODUCTION:
    # Production-specific logic
    pass

# Required environment variables
api_key = config.OPENAI_API_KEY  # Raises error if not set
db_url = config.SUPABASE_URL
```

### Error Handling & Logging

#### Structured Logging
```python
from utils.logger import logger, structlog

# Standard logging
logger.info("Agent execution started", agent_id=agent_id, user_id=user_id)

# Context-aware logging
structlog.contextvars.bind(thread_id=thread_id, agent_id=agent_id)
logger.error("Tool execution failed", tool_name=tool_name, error=str(e))
```

#### Exception Handling
```python
from fastapi import HTTPException

@router.post("/agents")
async def create_agent(agent_data: AgentCreateRequest):
    try:
        agent = await agent_service.create_agent(agent_data)
        return AgentResponse.from_orm(agent)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error creating agent: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Key Service Patterns

### Billing Integration
- `services/billing.py` - Stripe subscription management
- Usage tracking with Redis counters
- Billing status validation before agent execution

### Trigger System
- `triggers/` - Event-driven agent automation
- Scheduled triggers via APScheduler
- Webhook triggers for external integrations

### MCP (Model Context Protocol) Integration
- `agent/tools/mcp_tool_wrapper.py` - External tool integration
- Dynamic tool registration from MCP servers
- Secure credential management for external services

### Agent Versioning System
- Multiple agent versions in `agent_versions` table
- Configuration inheritance and overrides
- Version-specific tool and prompt management

## Testing Strategies

### Unit Testing with pytest
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_agent_creation():
    # Mock dependencies
    with patch('services.supabase.DBConnection') as mock_db:
        mock_client = AsyncMock()
        mock_db.return_value.client = mock_client
        
        # Test implementation
        result = await create_agent(agent_data)
        assert result.name == agent_data.name
```

### Integration Testing
```python
@pytest.mark.asyncio
async def test_agent_execution_flow():
    """Test complete agent execution with real database."""
    # Setup test data
    agent = await create_test_agent()
    thread = await create_test_thread()
    
    # Execute agent
    responses = []
    async for response in run_agent(agent.id, "test message"):
        responses.append(response)
    
    # Validate results
    assert len(responses) > 0
    assert responses[-1]["type"] == "message"
```

## Security Implementation

### Row Level Security (RLS)
All user data protected by RLS policies:
```sql
-- Example RLS policy
CREATE POLICY "Users can access their account's agents" ON agents
    FOR ALL USING (
        account_id = ANY(basejump.get_account_ids_for_current_user())
    );
```

### Credential Management
- Sensitive data encrypted using Fernet (`utils/encryption.py`)
- API keys stored in encrypted JSONB columns
- Environment variables for service credentials

### Input Validation
- Pydantic models for all request/response validation
- SQL injection prevention through parameterized queries
- Rate limiting via Redis-based IP tracking

## Performance Optimization

### Async Patterns
```python
# Proper async/await usage
async def process_multiple_agents(agent_ids: List[str]):
    tasks = [process_agent(agent_id) for agent_id in agent_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### Caching Strategy
- Redis caching for frequently accessed data
- Query result caching with TTL
- User session caching for authentication

### Database Optimization
- Proper indexing on foreign keys and query columns
- Connection pooling via Supabase client
- Bulk operations for batch processing

## Key Service Integrations

### Sandbox Environment
- Docker-isolated execution environments
- Browser automation via `sb_browser_tool.py`
- File system access via `sb_files_tool.py`
- Shell command execution via `sb_shell_tool.py`

### External Tool Integration
- Composio integration for third-party tools
- MCP (Model Context Protocol) server integration
- Data provider tools for external APIs

### Monitoring & Observability
- Langfuse for LLM call tracing and analytics
- Sentry for error tracking and performance monitoring
- Prometheus metrics for system health
- Structured logging with context propagation

## Development Guidelines

### Code Quality Standards
- Use type hints for all functions and class methods
- Follow async/await patterns for I/O operations
- Implement proper error handling with specific exception types
- Use Pydantic models for data validation
- Follow PEP 8 style guidelines

### Database Interaction Patterns
- Use parameterized queries to prevent SQL injection
- Implement proper transaction handling
- Use RLS policies for access control
- Follow migration best practices with idempotent operations

### Tool Development Best Practices
- Extend appropriate base classes (`AgentBuilderBaseTool` or `Tool`)
- Use `@openapi_schema` decorator for schema definition
- Implement comprehensive error handling
- Return structured `ToolResult` objects
- Log execution context and errors

### Testing Requirements
- Unit tests for business logic functions
- Integration tests for API endpoints
- Mock external dependencies appropriately
- Test error conditions and edge cases
- Maintain test coverage for critical paths

## Important Configuration

### Environment Variables
- `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` - Database connection
- `REDIS_URL` - Cache connection
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` - LLM providers
- `STRIPE_SECRET_KEY` - Billing integration
- `ENCRYPTION_KEY` - Credential encryption

### Feature Flags
Use `flags/flags.py` for feature toggles:
```python
from flags.flags import is_enabled

if is_enabled("new_feature", account_id=account_id):
    # New feature implementation
    pass
```

### Agent Configuration
Agent behavior controlled via JSONB config in `agents` table:
- `system_prompt` - Custom agent instructions
- `model_name` - LLM model selection
- `tools` - Enabled tool list
- `max_iterations` - Execution limits
- `enable_thinking` - Reasoning mode toggle