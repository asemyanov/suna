#!/usr/bin/env python3
"""
Complete token table for all tools showing detailed breakdown.
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

def create_complete_table():
    """Create a complete table showing all tools with detailed token breakdown"""
    
    print("🔧 COMPLETE TOOL TOKEN BREAKDOWN TABLE")
    print("=" * 95)
    print(f"{'Tool Name':<25} {'Description':<8} {'Schema':<8} {'Usage Example':<12} {'Total Tokens':<12} {'% of Total':<10}")
    print("-" * 95)
    
    total_tokens = 0
    tool_data = []
    
    # Calculate tokens for each tool
    for tool_name, details in TOOL_DETAILS.items():
        desc_tokens = rough_token_count(details["description"])
        schema_tokens = details["schema_tokens"]
        example_tokens = rough_token_count(details["usage_example"])
        tool_total = desc_tokens + schema_tokens + example_tokens
        total_tokens += tool_total
        
        tool_data.append({
            'name': tool_name,
            'desc_tokens': desc_tokens,
            'schema_tokens': schema_tokens,
            'example_tokens': example_tokens,
            'total_tokens': tool_total
        })
    
    # Sort by total tokens (highest first)
    tool_data.sort(key=lambda x: x['total_tokens'], reverse=True)
    
    # Display table
    for tool in tool_data:
        percentage = (tool['total_tokens'] / total_tokens) * 100
        print(f"{tool['name']:<25} {tool['desc_tokens']:<8} {tool['schema_tokens']:<8} {tool['example_tokens']:<12} {tool['total_tokens']:<12} {percentage:<9.1f}%")
    
    print("-" * 95)
    print(f"{'TOTAL (ALL 10 TOOLS)':<25} {'':<8} {'':<8} {'':<12} {total_tokens:<12} {'100.0%':<10}")
    print("=" * 95)
    
    # Summary statistics
    print(f"\n📊 SUMMARY STATISTICS:")
    print(f"  • Total Tokens (All Tools):     {total_tokens:,}")
    print(f"  • Average Tokens per Tool:      {total_tokens // len(TOOL_DETAILS):,}")
    print(f"  • Largest Tool:                 {tool_data[0]['name']} ({tool_data[0]['total_tokens']:,} tokens)")
    print(f"  • Smallest Tool:                {tool_data[-1]['name']} ({tool_data[-1]['total_tokens']:,} tokens)")
    
    # Component breakdown
    total_desc = sum(rough_token_count(details["description"]) for details in TOOL_DETAILS.values())
    total_schema = sum(details["schema_tokens"] for details in TOOL_DETAILS.values())
    total_examples = sum(rough_token_count(details["usage_example"]) for details in TOOL_DETAILS.values())
    
    print(f"\n🏗️  COMPONENT BREAKDOWN:")
    print(f"  • Total Description Tokens:     {total_desc:,} ({(total_desc/total_tokens)*100:.1f}%)")
    print(f"  • Total Schema Tokens:          {total_schema:,} ({(total_schema/total_tokens)*100:.1f}%)")
    print(f"  • Total Usage Example Tokens:   {total_examples:,} ({(total_examples/total_tokens)*100:.1f}%)")
    
    # Top 5 heaviest tools
    print(f"\n🏆 TOP 5 MOST TOKEN-HEAVY TOOLS:")
    for i, tool in enumerate(tool_data[:5], 1):
        print(f"  {i}. {tool['name']:<20}: {tool['total_tokens']:,} tokens ({(tool['total_tokens']/total_tokens)*100:.1f}%)")
    
    # Bottom 5 lightest tools
    print(f"\n🪶 TOP 5 LIGHTEST TOOLS:")
    for i, tool in enumerate(tool_data[-5:], 1):
        print(f"  {i}. {tool['name']:<20}: {tool['total_tokens']:,} tokens ({(tool['total_tokens']/total_tokens)*100:.1f}%)")
    
    return tool_data, total_tokens

if __name__ == "__main__":
    create_complete_table()