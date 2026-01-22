"""
api_bridge.py
=============
Google Gemini AI Integration Module

This module handles all interactions with Google's Generative AI (Gemini) API.
It provides intelligent supply chain analysis and recommendations based on 
inventory data using advanced prompt engineering and dynamic model selection.

Features:
- Automatic model discovery and fallback
- Rate limit handling with exponential backoff
- Free tier optimization
- Comprehensive error handling with diagnostics

Author: InsightPro Team
Version: 2.1
"""

import google.generativeai as genai
import os
import streamlit as st
import time

def get_supply_chain_brief(inventory_df, api_key):
    """
    Generates a comprehensive, AI-powered supply chain brief with detailed analysis.
    Uses advanced prompting for rich, actionable insights.
    """
    if not api_key:
        return "🔒 **AI Insights Locked**: Please enter your API Key in the sidebar."
        
    genai.configure(api_key=api_key)
    
    # 1. Enhanced Data Analysis
    inventory_df['stock_ratio'] = inventory_df['current_stock'] / inventory_df['reorder_point']
    critical_items = inventory_df.sort_values('stock_ratio').head(10)
    
    # Calculate additional metrics for richer context
    total_inventory_value = (inventory_df['current_stock'] * inventory_df['unit_cost']).sum()
    critical_value = (critical_items['current_stock'] * critical_items['unit_cost']).sum()
    avg_stock_ratio = inventory_df['stock_ratio'].mean()
    
    data_summary = critical_items[['product_name', 'current_stock', 'reorder_point', 'unit_cost']].to_string(index=False)
    
    prompt = f"""You are a Senior Supply Chain Strategy Advisor with expertise in inventory optimization and procurement planning.

INVENTORY ANALYSIS DATA:
{data_summary}

CONTEXT METRICS:
- Total Inventory Value: ${total_inventory_value:,.2f}
- Critical Items Value at Risk: ${critical_value:,.2f}
- Average Stock Health Ratio: {avg_stock_ratio:.2f}x

TASK: Provide a comprehensive **Supply Chain Strategy Brief** that includes:

1. **🔴 CRITICAL ALERTS** - List 2-3 products requiring immediate action with specific actions
2. **💰 CAPITAL IMPACT** - Quantify financial risk and procurement investment needed
3. **📊 OPTIMIZATION STRATEGY** - 2-3 specific, actionable recommendations
4. **⏱️ TIMELINE** - Priority sequence for procurement/restocking

FORMATTING REQUIREMENTS:
- Use clear markdown formatting with headers and bullet points
- Be specific with numbers and percentages
- Include timeframe estimates (e.g., "within 48 hours", "next 2 weeks")
- Keep tone professional but conversational
- Maximum 200 words total
- Focus on value-creation, not just warnings"""
    
    # 2. Dynamic Model Discovery (Fail-Safe) - Prioritize Free Tier Models
    valid_model_name = 'gemini-2.5-flash' # Default fallback - FREE TIER with generous quotas
    
    try:
        # Attempt to list models to find the best available one
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # Priority Strategy: Prefer 2.5-Flash (free tier) > 2.0-Flash > Others
        # 2.5-Flash has the most generous free tier quotas
        model_priority = ['gemini-2.5-flash', 'gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro', 'gemini-pro']
        
        found_priority = False
        for priority in model_priority:
            for avail in available_models:
                if priority in avail:
                    valid_model_name = avail
                    found_priority = True
                    break
            if found_priority:
                break
                
    except Exception as e:
        # If listing models fails (e.g. strict permission scopes), we shouldn't crash.
        # We just silently fall back to trying the default 'gemini-2.5-flash' blindly.
        print(f"Model discovery warning: {e}")
        # We don't return here, we proceed to try generation with the default valid_model_name
    
    # 3. Generate Content with the chosen model - with retry logic
    max_retries = 2
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            model = genai.GenerativeModel(valid_model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_str = str(e)
            # Check if it's a quota/rate limit error (429)
            if '429' in error_str or 'quota' in error_str.lower():
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 3 ** retry_count  # Exponential backoff: 3s, then 9s
                    print(f"Rate limited. Retrying in {wait_time}s... (Attempt {retry_count}/{max_retries})")
                    time.sleep(wait_time)
                    continue
            
            # If we get here, it's a non-recoverable error or we've exhausted retries
            debug_info = f"""
        **Debug Diagnostics:**
        - **API Key Status**: {'Set' if api_key else 'Missing'} (Ends with: ...{api_key[-4:] if api_key else 'N/A'})
        - **Selected Model**: {valid_model_name}
        - **Available Models**: {available_models if 'available_models' in locals() else 'Could not list'}
        - **Error Detail**: {str(e)}
        """
            return f"⚠️ **Generation Failed**: {str(e)} \n\n {debug_info}"
    
    return "⚠️ **Generation Failed**: Quota exceeded after retries. Please try again later or upgrade your API plan."
