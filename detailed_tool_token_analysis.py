#!/usr/bin/env python3
"""
Detailed token analysis for individual tool descriptions and schemas.
Focuses specifically on Tool Descriptions & Schemas AND Tool Usage Examples.
"""

def rough_token_count(text: str) -> int:
    """Rough token estimation based on GPT tokenization rules."""
    if not text:
        return 0
    words = len(text.split())
    chars = len(text)
    token_estimate = max(words * 0.75, chars / 4)
    return int(token_estimate)

# Tool-specific descriptions and schemas based on actual codebase analysis
TOOL_DETAILS = {
    "sb_shell_tool": {
        "description": """Execute a shell command in the workspace directory. IMPORTANT: Commands are non-blocking by default and run in a tmux session. This is ideal for long-running operations like starting servers or build processes. Uses sessions to maintain state between commands. This tool is essential for running CLI tools, installing packages, and managing system operations.""",
        "schema_tokens": 850,  # OpenAPI schema with parameters like command, folder, session_name, blocking, timeout
        "usage_example": """<function_calls>
<invoke name="execute_command">
<parameter name="command">npm run dev</parameter>
<parameter name="session_name">dev_server</parameter>
</invoke>
</function_calls>

<!-- Example 2: Running in Specific Directory -->
<function_calls>
<invoke name="execute_command">
<parameter name="command">npm run build</parameter>
<parameter name="folder">frontend</parameter>
<parameter name="session_name">build_process</parameter>
</invoke>
</function_calls>

<!-- Example 3: Blocking command (wait for completion) -->
<function_calls>
<invoke name="execute_command">
<parameter name="command">npm install</parameter>
<parameter name="blocking">true</parameter>
<parameter name="timeout">300</parameter>
</invoke>
</function_calls>"""
    },
    
    "browser_tool": {
        "description": """Advanced browser automation tool with screenshot capabilities, element interaction, and persistent session management. Can navigate websites, fill forms, click elements, take screenshots, and maintain browser state across multiple operations. Essential for web scraping, testing, and automated web interactions.""",
        "schema_tokens": 1200,  # Complex schema with navigation, clicking, form filling, screenshots
        "usage_example": """<function_calls>
<invoke name="navigate_to_page">
<parameter name="url">https://example.com</parameter>
<parameter name="take_screenshot">true</parameter>
</invoke>
</function_calls>

<!-- Example 2: Element Interaction -->
<function_calls>
<invoke name="click_element">
<parameter name="selector">button[type='submit']</parameter>
<parameter name="take_screenshot">true</parameter>
</invoke>
</function_calls>

<!-- Example 3: Form Filling -->
<function_calls>
<invoke name="fill_form_field">
<parameter name="selector">input[name='email']</parameter>
<parameter name="value">user@example.com</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_deploy_tool": {
        "description": """Deploy applications and services to various platforms including cloud providers, container registries, and hosting services. Supports automated deployment workflows, environment configuration, and service health monitoring.""",
        "schema_tokens": 600,  # Deployment parameters and configurations
        "usage_example": """<function_calls>
<invoke name="deploy_service">
<parameter name="platform">vercel</parameter>
<parameter name="project_path">./dist</parameter>
<parameter name="environment">production</parameter>
</invoke>
</function_calls>

<!-- Example 2: Container Deployment -->
<function_calls>
<invoke name="deploy_container">
<parameter name="image">myapp:latest</parameter>
<parameter name="platform">docker</parameter>
<parameter name="port">3000</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_expose_tool": {
        "description": """Expose local services and applications to the internet using tunneling services. Create public URLs for localhost development, webhook endpoints, and temporary service access. Supports multiple tunneling providers and custom domains.""",
        "schema_tokens": 400,  # Simple exposure parameters
        "usage_example": """<function_calls>
<invoke name="expose_service">
<parameter name="port">3000</parameter>
<parameter name="provider">ngrok</parameter>
<parameter name="custom_domain">myapp-dev</parameter>
</invoke>
</function_calls>

<!-- Example 2: Webhook Exposure -->
<function_calls>
<invoke name="expose_webhook">
<parameter name="port">8080</parameter>
<parameter name="path">/webhook</parameter>
</invoke>
</function_calls>"""
    },
    
    "web_search_tool": {
        "description": """Perform web searches using multiple search engines and APIs. Get real-time search results, news, academic papers, and specialized content. Supports advanced search operators, filtering, and result ranking.""",
        "schema_tokens": 500,  # Search parameters and filters
        "usage_example": """<function_calls>
<invoke name="web_search">
<parameter name="query">latest AI developments 2024</parameter>
<parameter name="num_results">10</parameter>
<parameter name="search_type">web</parameter>
</invoke>
</function_calls>

<!-- Example 2: News Search -->
<function_calls>
<invoke name="search_news">
<parameter name="query">climate change technology</parameter>
<parameter name="date_range">past_month</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_vision_tool": {
        "description": """Advanced computer vision capabilities for image analysis, object detection, OCR, and visual understanding. Can analyze screenshots, extract text from images, identify objects and people, and provide detailed visual descriptions.""",
        "schema_tokens": 700,  # Vision analysis parameters
        "usage_example": """<function_calls>
<invoke name="analyze_image">
<parameter name="image_path">screenshot.png</parameter>
<parameter name="analysis_type">detailed_description</parameter>
</invoke>
</function_calls>

<!-- Example 2: OCR Text Extraction -->
<function_calls>
<invoke name="extract_text">
<parameter name="image_path">document.jpg</parameter>
<parameter name="language">en</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_image_edit_tool": {
        "description": """Professional image editing and generation capabilities. Create, modify, resize, crop, and enhance images. Supports AI-powered image generation, background removal, style transfer, and advanced photo manipulation.""",
        "schema_tokens": 900,  # Complex image editing parameters
        "usage_example": """<function_calls>
<invoke name="generate_image">
<parameter name="prompt">futuristic cityscape at sunset</parameter>
<parameter name="style">photorealistic</parameter>
<parameter name="size">1024x1024</parameter>
</invoke>
</function_calls>

<!-- Example 2: Image Editing -->
<function_calls>
<invoke name="edit_image">
<parameter name="image_path">photo.jpg</parameter>
<parameter name="operation">remove_background</parameter>
<parameter name="output_path">edited_photo.png</parameter>
</invoke>
</function_calls>"""
    },
    
    "data_providers_tool": {
        "description": """Access data from major platforms including LinkedIn, Twitter, Amazon, Zillow, Yahoo Finance, and job boards. Retrieve user profiles, posts, product data, real estate information, financial data, and employment listings through official APIs.""",
        "schema_tokens": 800,  # Multiple provider schemas
        "usage_example": """<function_calls>
<invoke name="get_linkedin_profile">
<parameter name="profile_url">linkedin.com/in/username</parameter>
<parameter name="include_posts">true</parameter>
</invoke>
</function_calls>

<!-- Example 2: Stock Data -->
<function_calls>
<invoke name="get_stock_data">
<parameter name="symbol">AAPL</parameter>
<parameter name="timeframe">1d</parameter>
<parameter name="provider">yahoo_finance</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_sheets_tool": {
        "description": """Comprehensive spreadsheet operations for Google Sheets, Excel, and CSV files. Create, read, update, and analyze spreadsheet data. Supports formulas, charts, pivot tables, and automated data processing workflows.""",
        "schema_tokens": 650,  # Spreadsheet operation parameters
        "usage_example": """<function_calls>
<invoke name="create_spreadsheet">
<parameter name="name">Sales Report</parameter>
<parameter name="headers">["Date", "Product", "Revenue"]</parameter>
</invoke>
</function_calls>

<!-- Example 2: Data Analysis -->
<function_calls>
<invoke name="analyze_sheet_data">
<parameter name="sheet_id">abc123</parameter>
<parameter name="analysis_type">summary_statistics</parameter>
</invoke>
</function_calls>"""
    },
    
    "sb_files_tool": {
        "description": """Complete file system operations including reading, writing, copying, moving, and organizing files and directories. Supports text files, binary files, archives, and batch operations. Essential for file management and data processing.""",
        "schema_tokens": 550,  # File operation parameters
        "usage_example": """<function_calls>
<invoke name="read_file">
<parameter name="file_path">data.txt</parameter>
<parameter name="encoding">utf-8</parameter>
</invoke>
</function_calls>

<!-- Example 2: File Operations -->
<function_calls>
<invoke name="write_file">
<parameter name="file_path">output.json</parameter>
<parameter name="content">{"result": "success"}</parameter>
</invoke>
</function_calls>"""
    }
}

def calculate_tool_tokens():
    """Calculate token usage for tool descriptions, schemas, and usage examples"""
    
    # Original configuration (all tools enabled)
    original_tools = {
        "sb_shell_tool": True,
        "browser_tool": True,
        "sb_deploy_tool": True,
        "sb_expose_tool": True,
        "web_search_tool": True,
        "sb_vision_tool": True,
        "sb_image_edit_tool": True,
        "data_providers_tool": True,
        "sb_sheets_tool": True,
        "sb_files_tool": True,
    }
    
    # New optimized configuration
    optimized_tools = {
        "sb_shell_tool": True,
        "browser_tool": False,  # DISABLED
        "sb_deploy_tool": True,
        "sb_expose_tool": True,
        "web_search_tool": True,
        "sb_vision_tool": True,
        "sb_image_edit_tool": True,
        "data_providers_tool": False,  # DISABLED
        "sb_sheets_tool": True,
        "sb_files_tool": True,
    }
    
    print("🔧 DETAILED TOOL TOKEN ANALYSIS")
    print("=" * 60)
    
    original_total = 0
    optimized_total = 0
    
    print(f"{'Tool Name':<25} {'Status':<12} {'Desc':<8} {'Schema':<8} {'Example':<8} {'Total':<8}")
    print("-" * 75)
    
    for tool_name, tool_data in TOOL_DETAILS.items():
        desc_tokens = rough_token_count(tool_data["description"])
        schema_tokens = tool_data["schema_tokens"]
        example_tokens = rough_token_count(tool_data["usage_example"])
        tool_total = desc_tokens + schema_tokens + example_tokens
        
        # Original configuration (all enabled)
        if original_tools[tool_name]:
            original_total += tool_total
            original_status = "ENABLED"
        else:
            original_status = "DISABLED"
        
        # Optimized configuration
        if optimized_tools[tool_name]:
            optimized_total += tool_total
            optimized_status = "ENABLED"
        else:
            optimized_status = "DISABLED"
        
        # Show current status in optimized config
        status_color = optimized_status
        if optimized_status == "DISABLED":
            status_color = "🔴 DISABLED"
        else:
            status_color = "🟢 ENABLED"
        
        print(f"{tool_name:<25} {status_color:<12} {desc_tokens:<8} {schema_tokens:<8} {example_tokens:<8} {tool_total:<8}")
    
    print("-" * 75)
    print(f"{'ORIGINAL TOTAL (all tools)':<25} {'ALL ON':<12} {'':<8} {'':<8} {'':<8} {original_total:<8}")
    print(f"{'OPTIMIZED TOTAL':<25} {'SELECTIVE':<12} {'':<8} {'':<8} {'':<8} {optimized_total:<8}")
    
    savings = original_total - optimized_total
    savings_percent = (savings / original_total) * 100
    
    print("=" * 60)
    print(f"💰 TOKEN SAVINGS ANALYSIS:")
    print(f"  Original Total:     {original_total:,} tokens")
    print(f"  Optimized Total:    {optimized_total:,} tokens")
    print(f"  Total Savings:      {savings:,} tokens")
    print(f"  Percentage Saved:   {savings_percent:.1f}%")
    
    print(f"\n🔴 DISABLED TOOLS:")
    disabled_savings = 0
    for tool_name, enabled in optimized_tools.items():
        if not enabled:
            tool_data = TOOL_DETAILS[tool_name]
            desc_tokens = rough_token_count(tool_data["description"])
            schema_tokens = tool_data["schema_tokens"]
            example_tokens = rough_token_count(tool_data["usage_example"])
            tool_total = desc_tokens + schema_tokens + example_tokens
            disabled_savings += tool_total
            print(f"  • {tool_name:<20}: {tool_total:,} tokens saved")
    
    print(f"\n📊 BREAKDOWN OF SAVINGS:")
    print(f"  • browser_tool:        {TOOL_DETAILS['browser_tool']['schema_tokens'] + rough_token_count(TOOL_DETAILS['browser_tool']['description']) + rough_token_count(TOOL_DETAILS['browser_tool']['usage_example']):,} tokens")
    print(f"  • data_providers_tool: {TOOL_DETAILS['data_providers_tool']['schema_tokens'] + rough_token_count(TOOL_DETAILS['data_providers_tool']['description']) + rough_token_count(TOOL_DETAILS['data_providers_tool']['usage_example']):,} tokens")
    
    print(f"\n💡 IMPACT ANALYSIS:")
    print(f"  • Cost Savings: ~${(savings * 15 / 1000000):.4f} per request")
    print(f"  • Latency Improvement: ~{(savings/1000):.1f}s faster prompt processing")
    print(f"  • Remaining Tools: {sum(optimized_tools.values())}/10 tools active")
    
    return {
        'original_total': original_total,
        'optimized_total': optimized_total,
        'savings': savings,
        'savings_percent': savings_percent,
        'disabled_tools': [k for k, v in optimized_tools.items() if not v]
    }

if __name__ == "__main__":
    calculate_tool_tokens()