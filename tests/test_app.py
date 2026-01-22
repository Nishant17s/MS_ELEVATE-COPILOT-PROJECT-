"""
Unit tests for main application module.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_imports():
    """Test that all required modules can be imported."""
    try:
        import streamlit as st
        import pandas as pd
        import plotly.express as px
        from engine import db_manager, ml_logic
        from api_bridge import get_supply_chain_brief
        assert True
    except ImportError as e:
        pytest.fail(f"Import failed: {e}")


def test_app_file_exists():
    """Test that app.py exists and is readable."""
    app_path = Path(__file__).parent.parent / 'app.py'
    assert app_path.exists()
    assert app_path.is_file()


def test_engine_modules_exist():
    """Test that engine modules exist."""
    engine_path = Path(__file__).parent.parent / 'engine'
    assert engine_path.exists()
    assert (engine_path / 'db_manager.py').exists()
    assert (engine_path / 'ml_logic.py').exists()


def test_api_bridge_exists():
    """Test that API bridge module exists."""
    api_path = Path(__file__).parent.parent / 'api_bridge.py'
    assert api_path.exists()


def test_style_css_exists():
    """Test that style.css exists."""
    style_path = Path(__file__).parent.parent / 'style.css'
    assert style_path.exists()


def test_requirements_txt_exists():
    """Test that requirements.txt exists."""
    req_path = Path(__file__).parent.parent / 'requirements.txt'
    assert req_path.exists()
    
    # Read and verify it has content
    with open(req_path, 'r') as f:
        content = f.read()
        assert len(content) > 0
        assert 'streamlit' in content.lower()
