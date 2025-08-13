# MEVO AI Agent: Initial Prompt Token Analysis Report

## Executive Summary

The MEVO AI agent system creates an extensive initial prompt that ranges from **12,000 to 18,000+ tokens** before any user input is processed. This analysis reveals how a simple user prompt triggers the construction of a comprehensive system prompt that includes tool descriptions, usage examples, integration instructions, and context information.

## Prompt Construction Architecture

### 1. Dynamic Prompt Builder (`PromptManager.build_system_prompt()`)
Located in: `/backend/agent/run.py:224-304`

The system constructs prompts dynamically based on:
- **Agent Type**: Regular agent vs Agent Builder mode
- **Model Type**: Anthropic vs non-Anthropic (adds sample responses)
- **Tool Configuration**: Enabled/disabled tools per agent
- **MCP Integrations**: Active Model Context Protocol servers
- **Runtime Context**: Current date/time information

### 2. Core Prompt Components

#### Base System Prompt (`/backend/agent/prompt.py`)
- **Tokens**: ~1,700
- **Content**: Core agent identity, capabilities, execution environment, workflow management
- **Key Sections**:
  - Core identity & capabilities
  - Execution environment setup
  - Tool selection principles
  - Data processing & extraction rules
  - Workflow management instructions
  - Communication protocols
  - Self-configuration capabilities

#### Agent Builder Prompt (`/backend/agent/agent_builder_prompt.py`)
- **Tokens**: ~1,400
- **Purpose**: Special prompt for agents that build other agents
- **Content**: Integration workflows, credential management, MCP server interactions

## Token Breakdown Analysis

```
🎯 TOTAL ESTIMATED TOKENS: 12,230-18,000+

📊 TOKEN BREAKDOWN BY CATEGORY:
• Core System Instructions      : 1,699 tokens (13.9%)
• Agent Builder Instructions    : 1,356 tokens (11.1%)
• Tool Descriptions & Schemas   : 5,902 tokens (48.3%)
• Tool Usage Examples           : 1,845 tokens (15.1%)
• MCP Integration Info          :   359 tokens (2.9%)
• DateTime & Context Info       :   568 tokens (4.6%)
• Sample Responses              :     1 tokens (0.0%)
```

## Major Token Contributors

### 1. Tool Descriptions & Schemas (48.3% - ~6,000 tokens)

**Default Tool Set** (`/backend/agent/suna/config.py:13-24`):
- `sb_shell_tool` - Shell command execution
- `browser_tool` - Web browser automation
- `sb_deploy_tool` - Deployment operations
- `sb_expose_tool` - Service exposure
- `web_search_tool` - Web search capabilities
- `sb_vision_tool` - Image processing
- `sb_image_edit_tool` - Image editing
- `data_providers_tool` - LinkedIn, Twitter, etc.
- `sb_sheets_tool` - Spreadsheet operations
- `sb_files_tool` - File operations

**Each tool includes**:
- OpenAPI schema definition (~200-800 tokens)
- Detailed parameter descriptions
- Usage constraints and examples
- Integration instructions

### 2. Tool Usage Examples (15.1% - ~1,800 tokens)

Each tool provides XML-formatted usage examples:
```xml
<function_calls>
<invoke name="execute_command">
<parameter name="command">npm run dev</parameter>
<parameter name="session_name">dev_server</parameter>
</invoke>
</function_calls>
```

### 3. Core System Instructions (13.9% - ~1,700 tokens)

Comprehensive instructions covering:
- Agent identity and capabilities
- Execution environment setup
- Workflow management rules
- Communication protocols
- Data processing guidelines

## Dynamic Content Additions

### MCP (Model Context Protocol) Integration
When MCP servers are configured, additional content is added:
- MCP tool descriptions and schemas
- Integration instructions
- Critical usage guidelines
- Security warnings

**Estimated Addition**: 1,000-3,000+ tokens per active MCP integration

### Context Information
- Current date/time: ~70 tokens
- Browser state information: Variable
- Image context: Variable
- Temporary messages: Variable

### Model-Specific Content
- **Non-Anthropic Models**: Sample response examples added
- **Gemini Models**: Special prompt adaptations
- **Agent Builder Mode**: Additional 1,400 tokens

## Prompt Assembly Process

### 1. Base Prompt Selection
```python
# From run.py:230-246
if "gemini-2.5-flash" in model_name.lower():
    default_system_content = get_gemini_system_prompt()
else:
    default_system_content = get_system_prompt()

if is_agent_builder:
    system_content = get_agent_builder_prompt()
elif agent_config and agent_config.get('system_prompt'):
    system_content = render_prompt_template(agent_config['system_prompt'])
else:
    system_content = default_system_content
```

### 2. Tool Integration
Tools are registered based on configuration:
```python
# From run.py:417-444
if enabled_tools is None:
    tool_manager.register_all_tools()  # All 10+ tools
else:
    tool_manager.register_custom_tools(enabled_tools)  # Selective tools
```

### 3. MCP Integration
```python
# From run.py:248-291
if agent_config and (mcp_configs) and mcp_wrapper_instance:
    # Adds 1,000+ tokens of MCP instructions
    mcp_info = build_mcp_instructions(mcp_wrapper_instance)
    system_content += mcp_info
```

### 4. Context Injection
```python
# From run.py:293-302
datetime_info = build_datetime_context()
system_content += datetime_info
```

## Token Optimization Opportunities

### 1. Conditional Tool Loading
**Current**: All 10 tools loaded by default
**Optimization**: Load tools based on:
- User intent analysis
- Historical usage patterns
- Explicit tool requests

**Potential Savings**: 3,000-5,000 tokens

### 2. Compressed Tool Descriptions
**Current**: Verbose OpenAPI schemas and examples
**Optimization**: 
- Minimal schemas with core parameters only
- Consolidated usage examples
- Dynamic example loading

**Potential Savings**: 2,000-3,000 tokens

### 3. Smart MCP Integration
**Current**: Full MCP instructions added when any MCP is active
**Optimization**: 
- MCP-specific instructions only
- Lazy loading of MCP documentation
- Context-aware MCP tool selection

**Potential Savings**: 500-2,000 tokens

### 4. Template-Based Prompts
**Current**: Full prompt reconstruction each time
**Optimization**:
- Cached prompt templates
- Variable substitution
- Incremental prompt building

## Performance Implications

### Token Costs
- **Input Tokens**: 12,000-18,000 per request
- **Cost Impact**: ~$0.18-0.27 per request (at $15/1M tokens)
- **Daily Volume Impact**: Scales linearly with request volume

### Latency Impact
- **Processing Time**: Additional 1-3 seconds for prompt processing
- **Model Performance**: Larger context may affect response quality
- **Memory Usage**: Higher GPU memory requirements

## Recommendations

### Short-term Optimizations
1. **Implement conditional tool loading** based on user intent
2. **Compress tool usage examples** to essential patterns only
3. **Cache frequently used prompt components**
4. **Optimize MCP integration** to load only when needed

### Medium-term Improvements
1. **Implement prompt templates** with variable substitution
2. **Create tool usage analytics** to identify most/least used tools
3. **Implement smart context management**
4. **Add prompt compression algorithms**

### Long-term Architecture Changes
1. **Multi-tier prompt system** with basic/advanced modes
2. **Dynamic tool discovery** based on conversation context  
3. **Personalized tool configurations** per user
4. **AI-driven prompt optimization**

## Conclusion

The MEVO AI agent system creates comprehensive, feature-rich initial prompts that provide extensive capabilities but at a significant token cost. The 18,000-token initial prompt primarily consists of tool descriptions (48%) and usage examples (15%), indicating that tool management is the primary optimization opportunity.

Implementing conditional tool loading and compressed descriptions could reduce token usage by 40-60% while maintaining system capabilities for most use cases. This would significantly improve both cost efficiency and response latency while preserving the system's powerful multi-tool capabilities.

---

**Analysis Date**: August 12, 2025  
**System Version**: Based on commit `c7d1b53f`  
**Total Files Analyzed**: 25+ core system files