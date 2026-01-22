"""
InsightPro - Supply Chain Intelligence Dashboard
================================================

A premium SaaS-ready inventory management and supply chain intelligence platform.
Built with Streamlit, featuring real-time ML analytics and AI-powered insights.

Key Features:
- Real-time inventory monitoring with ML-based burn rate calculation
- AI-powered supply chain optimization via Google Gemini
- Interactive data editor with instant metric updates
- Predictive stockout analysis
- Premium UI/UX with glassmorphic design

Configuration:
- Environment: .env file with GEMINI_API_KEY
- Database: SQLite (auto-initialized with mock data)
- UI Styling: Custom CSS with modern design patterns

Author: InsightPro Team
Version: 2.1 SaaS Edition
Last Updated: January 22, 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from engine import db_manager, ml_logic
import api_bridge
import os
from dotenv import load_dotenv

# Load env immediately
load_dotenv()

# --- Configuration & Theme Injection ---
st.set_page_config(
    page_title="InsightPro",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# --- Logic Initialization ---
db_manager.init_db()
inventory_df = db_manager.get_inventory_df()
sales_df = db_manager.get_sales_df()

# --- Top Header & Settings ---
# We use columns to put settings in top right
col_brand, col_spacer, col_settings = st.columns([2, 4, 1.5], gap="small")

with col_brand:
    st.markdown("<h3 style='margin:0; padding-top:10px; color:#002D5B; font-size: 1.8rem;'>💠 InsightPro</h3>", unsafe_allow_html=True)
    st.markdown("<p style='margin:0; padding: 0; font-size: 0.85rem; color: #6B7280;'>Supply Chain Intelligence</p>", unsafe_allow_html=True)

# Initialize API Key from env
# Force reload from env to handle updates during runtime
env_key = os.getenv("GEMINI_API_KEY", "").strip()
if "api_key" not in st.session_state or st.session_state["api_key"] != env_key:
    st.session_state["api_key"] = env_key

with col_settings:
    st.write("")  # Spacer for alignment
    
    # Create custom SVG gear icon button
    with open("settings_icon.svg", "r") as f:
        svg_content = f.read()
    
    col_gear, _ = st.columns([1, 2])
    with col_gear:
        with st.popover("", help="Configure API keys and system settings"):
            st.markdown("**System Configuration**")
        # Text input defaults to current session state value
        api_key_input = st.text_input("Gemini API Key", value=st.session_state["api_key"], type="password", key="api_key_input_field")
        
        if api_key_input != st.session_state["api_key"]:
            st.session_state["api_key"] = api_key_input.strip()
            
        st.divider()
        st.caption(f"v2.1 SaaS Edition")

# --- Hero Section (SaaS Gradient) ---
critical_restocks = len(inventory_df[inventory_df['current_stock'] < inventory_df['reorder_point']])

st.markdown(f"""
    <div class="hero-container">
        <div class="hero-text-block">
            <div class="hero-title">📊 Inventory Intelligence</div>
            <div class="hero-subtitle">Real-time stock velocity analysis and AI-powered procurement recommendations.</div>
        </div>
        <div class="badge-container">
            <div class="badge-text">⚡ {critical_restocks} CRITICAL</div>
        </div>
    </div>
""", unsafe_allow_html=True)


# --- Main Layout (Grid + Sidebar/AI) ---
col_main, col_side = st.columns([5, 2], gap="large")

with col_side:
    st.markdown('<div class="card-container" style="padding: 20px;">', unsafe_allow_html=True)
    st.markdown("#### 📂 Data Management")
    st.caption("Import custom inventory data or use generated mock data")
    uploaded_file = st.file_uploader("Upload Inventory (CSV/Excel)", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith('.csv'):
                custom_df = pd.read_csv(uploaded_file)
            else:
                custom_df = pd.read_excel(uploaded_file)
            
            # Validation
            required = {'product_name', 'current_stock', 'reorder_point'}
            if not required.issubset(custom_df.columns):
                st.error(f"Missing columns: {required - set(custom_df.columns)}")
            else:
                # Normalize & Default Values
                if 'unit_cost' not in custom_df: custom_df['unit_cost'] = 0.0
                if 'selling_price' not in custom_df: custom_df['selling_price'] = 0.0
                if 'category' not in custom_df: custom_df['category'] = 'Uncategorized'
                if 'id' not in custom_df: custom_df['id'] = range(1, len(custom_df) + 1)
                
                # Replace Global Data
                inventory_df = custom_df
                # For custom data, we don't have sales history linked, so ML will return "No Data"
                sales_df = pd.DataFrame(columns=['product_id', 'sale_date', 'quantity_sold']) 
                st.success("Custom Data Loaded")
                
        except Exception as e:
            st.error(f"Error: {e}")
            
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # --- Asset Grid (Card Style) ---
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("#### 📋 Inventory Asset Grid")
    st.caption("📌 Edit stock levels directly. Real-time ML metrics auto-calculate below.")
    
    # ML Logic Loop
    burn_rates = []
    days_rem = []
    status_list = []
    
    for _, row in inventory_df.iterrows():
        ml_res = ml_logic.calculate_burn_rate_and_stockout(row, sales_df)
        burn_rates.append(ml_res['burn_rate'])
        days_rem.append(ml_res['days_to_stockout'])
        # Smart Status Logic
        if ml_res['days_to_stockout'] < 7:
            status_list.append("🔴 Critical") 
        elif ml_res['days_to_stockout'] < 30:
            status_list.append("🟡 Warning")
        else:
            status_list.append("🟢 Healthy")
            
    inventory_df['Burn Rate'] = burn_rates
    inventory_df['Runway'] = days_rem
    inventory_df['Status'] = status_list

    # Add summary metrics
    critical_count = len(inventory_df[inventory_df['Status'] == "🔴 Critical"])
    warning_count = len(inventory_df[inventory_df['Status'] == "🟡 Warning"])
    
    # Summary Cards
    col_crit, col_warn, col_value = st.columns(3)
    with col_crit:
        st.metric("🔴 Critical Items", critical_count, delta="needs immediate action", delta_color="inverse")
    with col_warn:
        st.metric("🟡 Warning Items", warning_count, delta="monitor closely", delta_color="off")
    with col_value:
        total_inv_value = (inventory_df['current_stock'] * inventory_df['unit_cost']).sum()
        st.metric("💰 Total Inventory Value", f"${total_inv_value:,.0f}", delta="at risk:", delta_color="off")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    edited_df = st.data_editor(
        inventory_df,
        column_config={
            "current_stock": st.column_config.NumberColumn(
                "Stock (Units)",
                min_value=0,
                step=1,
                format="%d"
            ),
            "Burn Rate": st.column_config.NumberColumn(
                "Burn Rate",
                format="%.1f / day"
            ),
            "Runway": st.column_config.NumberColumn(
                "Runway",
                format="%.1f days"
            ),
            "Status": st.column_config.TextColumn(
                "Health",
                width="small"
            )
        },
        disabled=["id", "Burn Rate", "Runway", "Status", "product_name", "category", "unit_cost", "selling_price", "reorder_point"],
        hide_index=True,
        width='stretch',
        height=450,
        key="data_editor"
    )
    
    # Save Logic
    if not inventory_df['current_stock'].equals(edited_df['current_stock']):
        db_manager.update_stock_batch(edited_df)
        st.toast("Stock levels updated.", icon="💾")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True) # End Card

    # --- Chart Section (Card Style) ---
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown("#### � Top 8 Burn Rate Analysis")
    
    chart_df = inventory_df.sort_values(by="Burn Rate", ascending=False).head(8)
    fig = px.bar(
        chart_df,
        x='product_name',
        y='Burn Rate',
        color='Runway',
        title="",
        color_continuous_scale=["#E63946", "#F59E0B", "#10B981"],
        template="plotly_white",
        labels={'Burn Rate': 'Daily Burn Rate (units/day)', 'product_name': 'Product'},
    )
    fig.update_layout(
        plot_bgcolor='rgba(245, 247, 250, 0.5)',
        paper_bgcolor='white',
        font={'family': "Inter", 'color': "#1A1F2C", 'size': 11},
        margin=dict(t=20, l=50, r=20, b=50),
        height=350,
        xaxis_tickangle=-45,
        hovermode='x unified',
        coloraxis_colorbar=dict(title="Runway<br>(days)")
    )
    fig.update_traces(marker_line_color='rgba(0, 45, 91, 0.2)', marker_line_width=1)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


with col_side:
    # --- AI Strategy Module (Glassmorphism) ---
    st.markdown("""
    <div class="ai-glass">
        <div class="ai-header">
            <span>🧠</span> AI Strategy Engine
        </div>
        <p style="font-size: 0.9rem; opacity: 0.85; margin-bottom: 22px; line-height: 1.6;">
            Powered by advanced machine learning to deliver actionable supply chain insights in real-time.
        </p>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Generate AI Brief", use_container_width=True, key="ai_brief_btn"):
        api_key = st.session_state.get("api_key")
        with st.spinner("🔄 Analyzing your inventory patterns..."):
            advice = api_bridge.get_supply_chain_brief(edited_df, api_key)
            st.markdown(f"""
                <div style="
                    margin-top: 20px; 
                    font-size: 0.95rem; 
                    line-height: 1.7;
                    padding: 16px;
                    background: linear-gradient(135deg, rgba(0, 174, 239, 0.05) 0%, rgba(0, 150, 136, 0.05) 100%);
                    border-left: 4px solid var(--accent-cyan);
                    border-radius: 8px;
                ">
                    {advice}
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True) # End AI Glass
